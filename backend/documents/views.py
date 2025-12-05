from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse, Http404
from django.db.models import Q
from .models import Document
from .serializers import DocumentSerializer, DocumentListSerializer
from accounts.models import User


class DocumentPermission(permissions.BasePermission):
    """
    Custom permission for documents:
    - All authenticated users can read
    - Only owner or admin can edit/delete
    """
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # Admins have full access
        if user.role == User.Role.ADMIN:
            return True
        
        # Check read access (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            # All authenticated users can read documents
            return True
        
        # Check write access (POST, PUT, PATCH, DELETE)
        # Only owner can edit/delete (admin already handled above)
        return obj.uploaded_by == user


class DocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and managing documents.
    
    list: Returns a list of all documents the user can access
    create: Upload a new document
    retrieve: Get document details
    update: Update document (owner or admin only)
    partial_update: Partially update document (owner or admin only)
    destroy: Delete document (owner or admin only)
    download: Download the document file
    """
    
    queryset = Document.objects.all()
    permission_classes = [permissions.IsAuthenticated, DocumentPermission]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DocumentListSerializer
        return DocumentSerializer
    
    def get_queryset(self):
        """
        Filter documents based on search and route_to.
        """
        queryset = Document.objects.all()
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(route_to__icontains=search)
            )
        
        # Filter by route_to
        route_to = self.request.query_params.get('route_to', None)
        if route_to:
            queryset = queryset.filter(route_to=route_to)
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        """Set the uploaded_by field to the current user"""
        serializer.save(uploaded_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        Download the document file.
        """
        document = self.get_object()
        
        # Check if file exists
        if not document.file:
            return Response(
                {'error': 'File not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            response = FileResponse(
                document.file.open(),
                content_type='application/octet-stream'
            )
            response['Content-Disposition'] = f'attachment; filename="{document.file_name}"'
            return response
        except (ValueError, OSError):
            return Response(
                {'error': 'Error opening file'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

