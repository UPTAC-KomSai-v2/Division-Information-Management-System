from rest_framework import serializers
from .models import (
    Communication,
    Memo,
    Circular,
    CommunicationDocument,
    CommunicationEvent
)
from accounts.models import User


class CommunicationSerializer(serializers.ModelSerializer):
    """Serializer for Communication parent model"""
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)
    created_by_name = serializers.SerializerMethodField()
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    is_published = serializers.BooleanField(read_only=True)
    
    # Child model data (will be populated based on type)
    memo_data = serializers.SerializerMethodField()
    circular_data = serializers.SerializerMethodField()
    document_data = serializers.SerializerMethodField()
    event_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Communication
        fields = [
            'communicationID',
            'type',
            'type_display',
            'title',
            'description',
            'created_by',
            'created_by_email',
            'created_by_name',
            'created_at',
            'published_at',
            'target_department',
            'target_roles',
            'is_published',
            'memo_data',
            'circular_data',
            'document_data',
            'event_data',
        ]
        read_only_fields = ['created_by', 'created_at']
    
    def get_created_by_name(self, obj):
        """Get creator's full name"""
        if obj.created_by:
            full_name = f"{obj.created_by.first_name} {obj.created_by.last_name}".strip()
            return full_name if full_name else obj.created_by.email
        return None
    
    def get_memo_data(self, obj):
        """Get memo child data if exists"""
        if hasattr(obj, 'memo'):
            return {
                'reqs_ack': obj.memo.reqs_ack
            }
        return None
    
    def get_circular_data(self, obj):
        """Get circular child data if exists"""
        if hasattr(obj, 'circular'):
            return {
                'reqs_ack': obj.circular.reqs_ack
            }
        return None
    
    def get_document_data(self, obj):
        """Get document child data if exists"""
        if hasattr(obj, 'document'):
            return {
                'document_ID': obj.document.document_ID,
                'route_to': obj.document.route_to
            }
        return None
    
    def get_event_data(self, obj):
        """Get event child data if exists"""
        if hasattr(obj, 'event'):
            return {
                'start_date': obj.event.start_date,
                'end_date': obj.event.end_date,
                'location': obj.event.location
            }
        return None
    
    def create(self, validated_data):
        """Override create to set created_by from request user"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class CommunicationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Communication
        fields = [
            'communicationID',
            'type',
            'type_display',
            'title',
            'description',
            'created_by_email',
            'created_at',
            'published_at',
            'target_department',
        ]


class MemoSerializer(serializers.ModelSerializer):
    """Serializer for Memo child model"""
    communication = CommunicationSerializer(read_only=True)
    
    class Meta:
        model = Memo
        fields = ['commID', 'reqs_ack', 'communication']
        read_only_fields = ['commID']


class CircularSerializer(serializers.ModelSerializer):
    """Serializer for Circular child model"""
    communication = CommunicationSerializer(read_only=True)
    
    class Meta:
        model = Circular
        fields = ['commID', 'reqs_ack', 'communication']
        read_only_fields = ['commID']


class CommunicationDocumentSerializer(serializers.ModelSerializer):
    """Serializer for CommunicationDocument child model"""
    communication = CommunicationSerializer(read_only=True)
    
    class Meta:
        model = CommunicationDocument
        fields = ['commID', 'document_ID', 'route_to', 'communication']
        read_only_fields = ['commID']


class CommunicationEventSerializer(serializers.ModelSerializer):
    """Serializer for CommunicationEvent child model"""
    communication = CommunicationSerializer(read_only=True)
    
    class Meta:
        model = CommunicationEvent
        fields = ['commID', 'start_date', 'end_date', 'location', 'communication']
        read_only_fields = ['commID']


class CommunicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating communication with child data"""
    
    # Child model fields (optional based on type)
    reqs_ack = serializers.BooleanField(required=False, write_only=True)
    document_ID = serializers.CharField(required=False, allow_blank=True, write_only=True)
    route_to = serializers.CharField(required=False, allow_blank=True, write_only=True)
    start_date = serializers.DateTimeField(required=False, write_only=True)
    end_date = serializers.DateTimeField(required=False, write_only=True)
    location = serializers.CharField(required=False, allow_blank=True, write_only=True)
    
    class Meta:
        model = Communication
        fields = [
            'type',
            'title',
            'description',
            'published_at',
            'target_department',
            'target_roles',
            'reqs_ack',
            'document_ID',
            'route_to',
            'start_date',
            'end_date',
            'location',
        ]
    
    def create(self, validated_data):
        # Extract child model data
        reqs_ack = validated_data.pop('reqs_ack', False)
        document_ID = validated_data.pop('document_ID', None)
        route_to = validated_data.pop('route_to', None)
        start_date = validated_data.pop('start_date', None)
        end_date = validated_data.pop('end_date', None)
        location = validated_data.pop('location', None)
        
        # Set created_by
        validated_data['created_by'] = self.context['request'].user
        
        # Create parent Communication
        communication = Communication.objects.create(**validated_data)
        
        # Create child model based on type
        comm_type = communication.type
        if comm_type == Communication.CommunicationType.MEMO:
            Memo.objects.create(commID=communication, reqs_ack=reqs_ack)
        elif comm_type == Communication.CommunicationType.CIRCULAR:
            Circular.objects.create(commID=communication, reqs_ack=reqs_ack)
        elif comm_type == Communication.CommunicationType.DOCUMENT:
            CommunicationDocument.objects.create(
                commID=communication,
                document_ID=document_ID,
                route_to=route_to
            )
        elif comm_type == Communication.CommunicationType.EVENT:
            if not start_date or not end_date:
                raise serializers.ValidationError("start_date and end_date are required for events")
            CommunicationEvent.objects.create(
                commID=communication,
                start_date=start_date,
                end_date=end_date,
                location=location
            )
        
        return communication

