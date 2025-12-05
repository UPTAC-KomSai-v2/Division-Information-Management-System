from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'title', 'status', 'priority', 'created_by', 'assigned_to', 'created_at']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['ticket_id', 'title', 'description', 'created_by__email']
    readonly_fields = ['ticket_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Ticket Information', {
            'fields': ('ticket_id', 'title', 'description', 'status', 'priority')
        }),
        ('Assignment', {
            'fields': ('created_by', 'assigned_to')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Make ticket_id read-only after creation"""
        if obj:  # Editing an existing object
            return self.readonly_fields
        else:  # Creating a new object
            return self.readonly_fields + ['ticket_id']
