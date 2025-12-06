from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, date
from .models import Event
from .serializers import EventSerializer, EventListSerializer
from accounts.models import User


class EventPermission(permissions.BasePermission):
    """
    Custom permission for events:
    - All authenticated users can view events
    - All authenticated users can create events
    - Only creator or admin can update/delete events
    """
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # Admins have full access
        if user.role == User.Role.ADMIN:
            return True
        
        # All authenticated users can view events
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Only creator or admin can update/delete
        return obj.created_by == user


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and managing calendar events.
    
    list: Returns a list of events (filtered by date range)
    create: Create a new event
    retrieve: Get event details
    update: Update event (creator or admin only)
    partial_update: Partially update event
    destroy: Delete event (creator or admin only)
    """
    
    queryset = Event.objects.all()
    permission_classes = [permissions.IsAuthenticated, EventPermission]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        return EventSerializer
    
    def get_queryset(self):
        """
        Filter events based on date range and other parameters.
        """
        queryset = Event.objects.all()
        
        # Filter by date (exact match)
        date_filter = self.request.query_params.get('date', None)
        if date_filter:
            try:
                # Parse date in format YYYY-MM-DD or YYYY/MM/DD
                date_str = date_filter.replace('/', '-')
                event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                queryset = queryset.filter(date=event_date)
            except ValueError:
                pass  # Invalid date format, ignore filter
        
        # Filter by date range
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        
        if date_from:
            try:
                date_from_str = date_from.replace('/', '-')
                from_date = datetime.strptime(date_from_str, '%Y-%m-%d').date()
                queryset = queryset.filter(date__gte=from_date)
            except ValueError:
                pass
        
        if date_to:
            try:
                date_to_str = date_to.replace('/', '-')
                to_date = datetime.strptime(date_to_str, '%Y-%m-%d').date()
                queryset = queryset.filter(date__lte=to_date)
            except ValueError:
                pass
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(venue__icontains=search)
            )
        
        # Filter upcoming events only
        upcoming_only = self.request.query_params.get('upcoming', None)
        if upcoming_only and upcoming_only.lower() == 'true':
            today = date.today()
            queryset = queryset.filter(date__gte=today)
        
        return queryset.order_by('date', 'start_time')
    
    def perform_create(self, serializer):
        """Set the created_by field to the current user"""
        serializer.save(created_by=self.request.user)

