from django.contrib import admin
from django import forms
from .models import Memo
from accounts.models import User


class MemoAdminForm(forms.ModelForm):
    """Custom form with checkbox field for target_roles"""
    
    target_roles_checkboxes = forms.MultipleChoiceField(
        choices=User.Role.choices,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Target Roles",
        help_text="Select one or more target roles"
    )
    
    class Meta:
        model = Memo
        exclude = ['target_roles', 'memo_id']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set initial values for checkboxes from JSON field
        if self.instance and self.instance.pk:
            if self.instance.target_roles:
                self.fields['target_roles_checkboxes'].initial = self.instance.target_roles
            else:
                self.fields['target_roles_checkboxes'].initial = []
        else:
            self.fields['target_roles_checkboxes'].initial = []
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Convert checkbox selections to JSON array
        selected_roles = cleaned_data.get('target_roles_checkboxes', [])
        cleaned_data['target_roles'] = selected_roles if selected_roles else []
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Set target_roles from checkboxes
        selected_roles = self.cleaned_data.get('target_roles_checkboxes', [])
        instance.target_roles = selected_roles if selected_roles else []
        
        if commit:
            instance.save()
        return instance


@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
    form = MemoAdminForm
    list_display = [
        'memo_id',
        'title',
        'target_department',
        'created_by',
        'created_at',
        'published_at',
        'reqs_ack',
        'is_published'
    ]
    list_filter = [
        'target_department',
        'reqs_ack',
        'created_at',
        'published_at'
    ]
    search_fields = [
        'title',
        'description',
        'memo_id',
        'target_department',
        'created_by__email',
        'created_by__first_name',
        'created_by__last_name'
    ]
    readonly_fields = ['memo_id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Memo Information', {
            'fields': ('title', 'description')
        }),
        ('Target Audience', {
            'fields': ('target_department', 'target_roles_checkboxes')
        }),
        ('Acknowledgment', {
            'fields': ('reqs_ack',)
        }),
        ('Author & Timestamps', {
            'fields': ('created_by', 'created_at', 'updated_at', 'published_at')
        }),
    )
    
    def is_published(self, obj):
        return obj.is_published
    is_published.boolean = True
    is_published.short_description = 'Published'

