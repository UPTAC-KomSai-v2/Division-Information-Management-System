from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'get_full_name', 'role', 'status', 'department', 'is_active', 'date_joined']
    list_filter = ['role', 'status', 'is_active', 'is_staff', 'department', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name', 'department']
    ordering = ['email']
    readonly_fields = ['date_joined', 'last_login']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'phone', 'avatar', 'bio')
        }),
        ('Work Info', {
            'fields': ('department', 'status')
        }),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role'),
        }),
        ('Personal Info', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name'),
        }),
    )
    
    def get_full_name(self, obj):
        """Return only first name and last name, no email fallback"""
        full_name = f"{obj.first_name} {obj.last_name}".strip()
        return full_name if full_name else "-"
    get_full_name.short_description = 'Name'
