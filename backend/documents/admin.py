from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'route_to', 'uploaded_by', 'created_at']
    list_filter = ['route_to', 'created_at']
    search_fields = ['name', 'description', 'route_to', 'uploaded_by__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Document Information', {
            'fields': ('name', 'file', 'description')
        }),
        ('Routing', {
            'fields': ('route_to',)
        }),
        ('Upload Information', {
            'fields': ('uploaded_by', 'created_at', 'updated_at')
        }),
    )

