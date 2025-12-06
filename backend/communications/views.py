from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from datetime import datetime

from .models import (
    Communication,
    Memo,
    Circular,
    CommunicationDocument,
    CommunicationEvent,
    ChatMessage
)
from .serializers import (
    CommunicationSerializer,
    CommunicationListSerializer,
    CommunicationCreateSerializer,
    MemoSerializer,
    CircularSerializer,
    CommunicationDocumentSerializer,
    CommunicationEventSerializer
)
from accounts.models import User
from rest_framework.views import APIView


class CommunicationPermission(permissions.BasePermission):
    """
    Custom permission for communications:
    - Anyone authenticated can read
    - Only creator or admin can modify
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # Read permissions allowed to all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Only creator or admin can modify
        return obj.created_by == user or user.role == User.Role.ADMIN


class CommunicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and managing communications.
    
    list: Returns a list of communications (filtered by type, department, etc.)
    create: Create a new communication with child model data
    retrieve: Get communication details including child data
    update: Update communication (creator or admin only)
    partial_update: Partially update communication
    destroy: Delete communication (creator or admin only)
    """
    
    queryset = Communication.objects.all()
    permission_classes = [permissions.IsAuthenticated, CommunicationPermission]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CommunicationCreateSerializer
        elif self.action == 'list':
            return CommunicationListSerializer
        return CommunicationSerializer
    
    def get_queryset(self):
        """Filter communications based on search and filters"""
        queryset = Communication.objects.all()
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(target_department__icontains=search)
            )
        
        # Filter by type
        comm_type = self.request.query_params.get('type', None)
        if comm_type:
            queryset = queryset.filter(type=comm_type)
        
        # Filter by department
        department = self.request.query_params.get('department', None)
        if department:
            queryset = queryset.filter(target_department=department)
        
        # Filter by target role
        role = self.request.query_params.get('role', None)
        if role:
            queryset = queryset.filter(target_roles__contains=[role])
        
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
        """Publish a communication"""
        communication = self.get_object()
        
        if communication.published_at:
            return Response(
                {'detail': 'Communication is already published.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        communication.published_at = timezone.now()
        communication.save()
        
        serializer = self.get_serializer(communication)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='unpublish')
    def unpublish(self, request, pk=None):
        """Unpublish a communication"""
        communication = self.get_object()
        communication.published_at = None
        communication.save()
        
        serializer = self.get_serializer(communication)
        return Response(serializer.data)


def _user_in_room(room_key: str, user_id: int) -> bool:
    """Check if a user id is one of the participants encoded in room_key."""
    try:
        parts = room_key.split("_")
        participants = {int(p) for p in parts}
        return user_id in participants
    except Exception:
        return False


class ChatHistoryView(APIView):
    """
    Delete chat history for a given conversation room.
    Only participants in the room can delete.
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, room):
        if not _user_in_room(room, request.user.id):
            return Response(
                {"detail": "Not permitted to delete this conversation."},
                status=status.HTTP_403_FORBIDDEN,
            )

        deleted_count, _ = ChatMessage.objects.filter(conversation_id=room).delete()
        return Response({"deleted": deleted_count})

