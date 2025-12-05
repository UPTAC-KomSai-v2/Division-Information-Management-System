from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from datetime import datetime

from .models import Memo
from .serializers import (
    MemoSerializer,
    MemoListSerializer
)
from accounts.models import User


class MemoPermission(permissions.BasePermission):
    """
    Custom permission for memos:
    - Anyone authenticated can read
    - Only creator or admin can modify
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # Read permissions allowed to all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Only creator or admin can modify
        return obj.created_by == user or user.role == User.Role.ADMIN


class MemoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and managing memos.
    
    list: Returns a list of memos (filtered by search, department, role, etc.)
    create: Create a new memo
    retrieve: Get memo details
    update: Update memo (creator or admin only)
    partial_update: Partially update memo
    destroy: Delete memo (creator or admin only)
    """
    
    queryset = Memo.objects.all()
    permission_classes = [permissions.IsAuthenticated, MemoPermission]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MemoListSerializer
        return MemoSerializer
    
    def get_queryset(self):
        """Filter memos based on search and filters"""
        queryset = Memo.objects.all()
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(memo_id__icontains=search) |
                Q(target_department__icontains=search)
            )
        
        # Filter by department
        department = self.request.query_params.get('department', None)
        if department:
            queryset = queryset.filter(target_department=department)
        
        # Filter by target role
        role = self.request.query_params.get('role', None)
        if role:
            queryset = queryset.filter(target_roles__contains=[role])
        
        # Filter by acknowledgment requirement
        reqs_ack = self.request.query_params.get('reqs_ack', None)
        if reqs_ack is not None:
            reqs_ack_bool = reqs_ack.lower() == 'true'
            queryset = queryset.filter(reqs_ack=reqs_ack_bool)
        
        # Filter by published status
        published = self.request.query_params.get('published', None)
        if published is not None:
            if published.lower() == 'true':
                queryset = queryset.exclude(published_at__isnull=True).filter(
                    published_at__lte=timezone.now()
                )
            else:
                queryset = queryset.filter(
                    Q(published_at__isnull=True) | Q(published_at__gt=timezone.now())
                )
        
        # Filter by date range
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        
        if date_from:
            try:
                date_from_str = date_from.replace('/', '-')
                from_date = datetime.strptime(date_from_str, '%Y-%m-%d').date()
                queryset = queryset.filter(created_at__gte=from_date)
            except ValueError:
                pass
        
        if date_to:
            try:
                date_to_str = date_to.replace('/', '-')
                to_date = datetime.strptime(date_to_str, '%Y-%m-%d').date()
                queryset = queryset.filter(created_at__lte=to_date)
            except ValueError:
                pass
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        """Set created_by to current user"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'], url_path='publish')
    def publish(self, request, pk=None):
        """Publish a memo"""
        memo = self.get_object()
        
        if memo.published_at:
            return Response(
                {'detail': 'Memo is already published.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        memo.published_at = timezone.now()
        memo.save()
        
        serializer = self.get_serializer(memo)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='unpublish')
    def unpublish(self, request, pk=None):
        """Unpublish a memo"""
        memo = self.get_object()
        memo.published_at = None
        memo.save()
        
        serializer = self.get_serializer(memo)
        return Response(serializer.data)

