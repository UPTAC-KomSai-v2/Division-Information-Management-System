from django.db import models
from django.conf import settings
import os


def document_upload_path(instance, filename):
    """Generate upload path for documents"""
    # Upload to: media/documents/{user_id}/{filename}
    return os.path.join('documents', str(instance.uploaded_by.id), filename)


class Document(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=document_upload_path)
    route_to = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Route To",
        help_text="The receiving end of the document"
    )
    description = models.TextField(blank=True, null=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_documents'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['route_to']),
        ]

    def __str__(self):
        return f"{self.name}"

    @property
    def file_size(self):
        """Returns file size in bytes"""
        if self.file:
            try:
                return self.file.size
            except (ValueError, OSError):
                return 0
        return 0

    @property
    def file_name(self):
        """Returns the original filename"""
        if self.file:
            return os.path.basename(self.file.name)
        return ""

