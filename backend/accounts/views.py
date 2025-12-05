from rest_framework import permissions, generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserSerializer, EmailTokenObtainPairSerializer
from .models import User


class MeView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        # Returns the currently authenticated user
        return self.request.user


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