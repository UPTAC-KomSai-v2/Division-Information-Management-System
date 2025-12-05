from rest_framework import serializers
from .models import Memo
from accounts.models import User


class MemoSerializer(serializers.ModelSerializer):
    """Serializer for Memo model"""
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)
    created_by_name = serializers.SerializerMethodField()
    is_published = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Memo
        fields = [
            'id',
            'memo_id',
            'title',
            'description',
            'created_by',
            'created_by_email',
            'created_by_name',
            'created_at',
            'updated_at',
            'reqs_ack',
            'target_department',
            'target_roles',
            'published_at',
            'is_published',
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'memo_id']
    
    def get_created_by_name(self, obj):
        """Get creator's full name"""
        if obj.created_by:
            full_name = f"{obj.created_by.first_name} {obj.created_by.last_name}".strip()
            return full_name if full_name else obj.created_by.email
        return None
    
    def create(self, validated_data):
        """Override create to set created_by from request user"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class MemoListSerializer(serializers.ModelSerializer):
    """Simplified serializer for memo list views"""
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)
    
    class Meta:
        model = Memo
        fields = [
            'id',
            'memo_id',
            'title',
            'description',
            'created_by_email',
            'created_at',
            'published_at',
            'target_department',
            'reqs_ack',
        ]

