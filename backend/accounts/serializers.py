from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    initials = serializers.CharField(read_only=True)
    avatar_url = serializers.SerializerMethodField()
    name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'name',
            'full_name',
            'initials',
            'role',
            'phone',
            'department',
            'avatar',
            'avatar_url',
            'bio',
            'status',
            'is_active',
        ]
        read_only_fields = ['id', 'email', 'date_joined']

    def get_avatar_url(self, obj):
        """Returns the full URL to the avatar"""
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None


class UserListSerializer(serializers.ModelSerializer):
    """Simplified serializer for directory listing"""
    name = serializers.CharField(source='get_full_name', read_only=True)
    initials = serializers.CharField(read_only=True)
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'name',
            'initials',
            'role',
            'status',
            'avatar_url',
        ]

    def get_avatar_url(self, obj):
        """Returns the full URL to the avatar"""
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'phone',
            'department',
            'avatar',
            'bio',
            'status',
        ]


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data