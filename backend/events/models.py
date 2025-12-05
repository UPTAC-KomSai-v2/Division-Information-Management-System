from django.db import models
from django.conf import settings


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    venue = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_events'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'start_time']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.title} - {self.date}"

    @property
    def creator_email(self):
        """Get creator's email"""
        return self.created_by.email if self.created_by else ""

