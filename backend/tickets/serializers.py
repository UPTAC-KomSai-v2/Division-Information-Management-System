from rest_framework import serializers
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source='created_by.email', read_only=True)
    creator_email = serializers.EmailField(read_only=True)
    assignee = serializers.CharField(source='assigned_to.email', read_only=True, allow_null=True)
    assignee_email = serializers.EmailField(read_only=True, allow_null=True)
    # expose created_at as datetime to avoid DRF date coercion assertion
    date = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id',
            'ticket_id',
            'title',
            'description',
            'status',
            'priority',
            'created_by',
            'creator',
            'creator_email',
            'assigned_to',
            'assignee',
            'assignee_email',
            'created_at',
            'date',
            'updated_at',
        ]
        read_only_fields = ['ticket_id', 'created_by', 'created_at', 'updated_at']


class TicketListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    creator = serializers.CharField(source='created_by.email', read_only=True)
    date = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id',
            'ticket_id',
            'title',
            'status',
            'priority',
            'creator',
            'date',
            'created_at',
        ]


class TicketCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tickets (title and description only)"""
    
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority']
