from rest_framework import permissions, generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Q

from .serializers import (
    UserSerializer,
    UserListSerializer,
    UserProfileUpdateSerializer,
    EmailTokenObtainPairSerializer
)
from .models import User


class MeView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        # Returns the currently authenticated user
        return self.request.user

    def get_serializer_context(self):
        """Add request to context for avatar URL generation"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class IsDivisionAdmin(permissions.BasePermission):
    """
    Custom permission: allows access only to division admins.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.DIVISION_ADMIN
        )


class AdminOnlyView(generics.GenericAPIView):
    """
    Example view just to test admin-only access.
    You can change the permission to IsDivisionAdmin if you want.
    """

    # If you want ONLY Django superusers:
    # permission_classes = [permissions.IsAdminUser]

    # If you want ONLY division admins based on your custom role:
    permission_classes = [IsDivisionAdmin]

    def get(self, request, *args, **kwargs):
        return Response({"detail": "You are an admin."})


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners or admins to update profiles.
    """
    
    def has_object_permission(self, request, view, obj):
        # Admins can update any profile
        if request.user.role == User.Role.ADMIN:
            return True
        
        # Users can only update their own profile
        return obj == request.user


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and managing user profiles (directory).
    
    list: Returns a list of all users (directory)
    retrieve: Get user profile details
    update: Update user profile (own profile or admin only)
    partial_update: Partially update user profile
    """
    
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        if self.action in ['update', 'partial_update']:
            return UserProfileUpdateSerializer
        return UserSerializer
    
    def get_queryset(self):
        """Filter users based on search and status"""
        queryset = User.objects.filter(is_active=True)
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(department__icontains=search)
            )
        
        # Filter by role
        role = self.request.query_params.get('role', None)
        if role:
            queryset = queryset.filter(role=role)
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by department
        department = self.request.query_params.get('department', None)
        if department:
            queryset = queryset.filter(department=department)
        
        return queryset.order_by('first_name', 'last_name', 'email')
    
    def get_serializer_context(self):
        """Add request to context for avatar URL generation"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_permissions(self):
        """
        Allow read access to all authenticated users,
        but only allow users to update their own profile (or admin to update any)
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update']:
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        return super().get_permissions()
    
    def retrieve(self, request, *args, **kwargs):
        """Get user profile details"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """Update user profile"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Return full user details after update
        updated_instance = User.objects.get(pk=instance.pk)
        response_serializer = UserSerializer(updated_instance, context={'request': request})
        return Response(response_serializer.data)