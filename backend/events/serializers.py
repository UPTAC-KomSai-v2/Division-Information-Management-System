from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source='created_by.email', read_only=True)
    creator_email = serializers.EmailField(read_only=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'description',
            'date',
            'start_time',
            'end_time',
            'venue',
            'created_by',
            'creator',
            'creator_email',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class EventListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    creator = serializers.CharField(source='created_by.email', read_only=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'description',
            'date',
            'creator',
        ]

