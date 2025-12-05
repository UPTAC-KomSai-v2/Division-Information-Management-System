from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Ticket
from .serializers import TicketSerializer, TicketListSerializer, TicketCreateSerializer
from accounts.models import User


class TicketPermission(permissions.BasePermission):
    """
    Custom permission for tickets:
    - All authenticated users can create tickets
    - Users can view their own tickets
    - Staff and Admin can view all tickets
    - Only creator, assignee, or admin can update tickets
    - Only admin can delete tickets
    """
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # Admins have full access
        if user.role == User.Role.ADMIN:
            return True
        
        # Check read access (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            # Users can view their own tickets
            if obj.created_by == user:
                return True
            # Staff can view all tickets
            if user.role == User.Role.STAFF:
                return True
            # Faculty can only view their own
            return False
        
        # Check write access (PUT, PATCH)
        # Creator, assignee, or staff/admin can update
        if obj.created_by == user:
            return True
        if obj.assigned_to == user:
            return True
        if user.role == User.Role.STAFF:
            return True
        
        return False


class TicketViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and managing support tickets.
    
    list: Returns a list of tickets (filtered by user role)
    create: Create a new ticket
    retrieve: Get ticket details
    update: Update ticket (creator, assignee, or staff/admin)
    partial_update: Partially update ticket
    destroy: Delete ticket (admin only)
    """
    
    queryset = Ticket.objects.all()
    permission_classes = [permissions.IsAuthenticated, TicketPermission]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TicketListSerializer
        if self.action == 'create':
            return TicketCreateSerializer
        return TicketSerializer
    
    def get_queryset(self):
        """
        Filter tickets based on user role.
        """
        user = self.request.user
        queryset = Ticket.objects.all()
        
        # Admin can see all tickets
        if user.role == User.Role.ADMIN:
            pass  # Return all tickets
        # Staff can see all tickets
        elif user.role == User.Role.STAFF:
            pass  # Return all tickets
        # Faculty can only see their own tickets
        else:
            queryset = queryset.filter(created_by=user)
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(ticket_id__icontains=search)
            )
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by priority
        priority_filter = self.request.query_params.get('priority', None)
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
        
        # Filter by assigned_to
        assigned_to = self.request.query_params.get('assigned_to', None)
        if assigned_to:
            queryset = queryset.filter(assigned_to_id=assigned_to)
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        """Set the created_by field to the current user"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['patch'])
    def assign(self, request, pk=None):
        """
        Assign ticket to a user.
        Body: {"assigned_to": <user_id>}
        """
        ticket = self.get_object()
        assigned_to_id = request.data.get('assigned_to', None)
        
        if assigned_to_id:
            try:
                user = User.objects.get(id=assigned_to_id)
                ticket.assigned_to = user
                ticket.save()
                serializer = self.get_serializer(ticket)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(
            {'error': 'assigned_to field is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['patch'])
    def close(self, request, pk=None):
        """
        Close a ticket (set status to CLOSED).
        """
        ticket = self.get_object()
        ticket.status = Ticket.Status.CLOSED
        ticket.save()
        serializer = self.get_serializer(ticket)
        return Response(serializer.data)
