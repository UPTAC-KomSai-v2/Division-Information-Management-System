from django.db import models
from django.conf import settings
from django.db.models import Max
from django.utils import timezone


class Memo(models.Model):
    """Memo model for internal communications"""
    
    memo_id = models.CharField(max_length=20, unique=True, editable=False, verbose_name="Memo ID")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_memos',
        verbose_name="Author"
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    reqs_ack = models.BooleanField(
        default=False,
        verbose_name="Requires Acknowledgment"
    )
    target_department = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Target Department"
    )
    target_roles = models.JSONField(
        default=list,
        blank=True,
        help_text="List of target roles (e.g., ['ADMIN', 'STAFF', 'FACULTY'])",
        verbose_name="Target Roles"
    )
    published_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Published At"
    )
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['memo_id']),
            models.Index(fields=['published_at']),
            models.Index(fields=['target_department']),
        ]
        verbose_name = "Memo"
        verbose_name_plural = "Memos"
    
    def __str__(self):
        return f"{self.memo_id} - {self.title}"
    
    def save(self, *args, **kwargs):
        """Auto-generate memo_id if not set"""
        if not self.memo_id:
            self.memo_id = self.generate_memo_id()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_memo_id():
        """Generate unique memo ID in format MEMO-001, MEMO-002, etc."""
        # Get the highest memo number
        last_memo = Memo.objects.aggregate(Max('memo_id'))
        last_id = last_memo.get('memo_id__max', None)
        
        if last_id:
            # Extract the number part (e.g., "MEMO-001" -> 1)
            try:
                last_num = int(last_id.split('-')[1])
                new_num = last_num + 1
            except (IndexError, ValueError):
                new_num = 1
        else:
            new_num = 1
        
        # Format as MEMO-XXX with leading zeros
        return f"MEMO-{new_num:03d}"
    
    @property
    def is_published(self):
        """Check if memo is published"""
        return self.published_at is not None and self.published_at <= timezone.now()
    
    @property
    def creator_email(self):
        """Get creator's email"""
        return self.created_by.email if self.created_by else ""

