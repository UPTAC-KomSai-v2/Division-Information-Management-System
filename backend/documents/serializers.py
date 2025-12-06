from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by_email = serializers.EmailField(source='uploaded_by.email', read_only=True)
    file_url = serializers.SerializerMethodField()
    file_size = serializers.IntegerField(read_only=True)
    file_name = serializers.CharField(read_only=True)

    class Meta:
        model = Document
        fields = [
            'id',
            'name',
            'file',
            'file_url',
            'file_name',
            'file_size',
            'route_to',
            'description',
            'uploaded_by',
            'uploaded_by_email',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['uploaded_by', 'created_at', 'updated_at']

    def get_file_url(self, obj):
        """Returns the full URL to the file"""
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None

    def create(self, validated_data):
        """Override create to set uploaded_by from request user"""
        validated_data['uploaded_by'] = self.context['request'].user
        return super().create(validated_data)


class DocumentListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    uploaded_by_email = serializers.EmailField(source='uploaded_by.email', read_only=True)
    file_url = serializers.SerializerMethodField()
    file_name = serializers.CharField(read_only=True)

    class Meta:
        model = Document
        fields = [
            'id',
            'name',
            'route_to',
            'uploaded_by_email',
            'created_at',
            'file_url',
            'file_name',
        ]

    def get_file_url(self, obj):
        """Returns the full URL to the file"""
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None

