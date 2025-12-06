from django.db import models
from django.conf import settings
from django.utils import timezone


class Communication(models.Model):
    """
    Parent model for all communication types (Circulars, Memos, Events, Documents)
    """
    
    class CommunicationType(models.TextChoices):
        CIRCULAR = "CIRCULAR", "Circular"
        MEMO = "MEMO", "Memo"
        EVENT = "EVENT", "Event"
        DOCUMENT = "DOCUMENT", "Document"
    
    # Primary fields
    communicationID = models.AutoField(primary_key=True, verbose_name="Communication ID")
    type = models.CharField(
        max_length=50,
        choices=CommunicationType.choices,
        verbose_name="Type"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    # Author and timestamps
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_communications',
        verbose_name="Author"
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")
    published_at = models.DateTimeField(blank=True, null=True, verbose_name="Published At")
    
    # Target audience
    target_department = models.CharField(max_length=255, blank=True, null=True, verbose_name="Target Department")
    target_roles = models.JSONField(
        default=list,
        blank=True,
        help_text="List of target roles (e.g., ['ADMIN', 'STAFF', 'FACULTY'])",
        verbose_name="Target Roles"
    )
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['type']),
            models.Index(fields=['published_at']),
            models.Index(fields=['target_department']),
        ]
        verbose_name = "Communication"
        verbose_name_plural = "Communications"
    
    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"
    
    @property
    def is_published(self):
        """Check if communication is published"""
        return self.published_at is not None and self.published_at <= timezone.now()


class Memo(models.Model):
    """
    Child model for Memo communications
    """
    commID = models.OneToOneField(
        Communication,
        on_delete=models.CASCADE,
        related_name='memo',
        primary_key=True,
        verbose_name="Communication ID"
    )
    reqs_ack = models.BooleanField(
        default=False,
        verbose_name="Requires Acknowledgment"
    )
    
    class Meta:
        verbose_name = "Memo"
        verbose_name_plural = "Memos"
    
    def __str__(self):
        return f"Memo: {self.commID.title}"


class Circular(models.Model):
    """
    Child model for Circular communications
    """
    commID = models.OneToOneField(
        Communication,
        on_delete=models.CASCADE,
        related_name='circular',
        primary_key=True,
        verbose_name="Communication ID"
    )
    reqs_ack = models.BooleanField(
        default=False,
        verbose_name="Requires Acknowledgment"
    )
    
    class Meta:
        verbose_name = "Circular"
        verbose_name_plural = "Circulars"
    
    def __str__(self):
        return f"Circular: {self.commID.title}"


class CommunicationDocument(models.Model):
    """
    Child model for Document communications
    """
    commID = models.OneToOneField(
        Communication,
        on_delete=models.CASCADE,
        related_name='document',
        primary_key=True,
        verbose_name="Communication ID"
    )
    document_ID = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Document ID"
    )
    route_to = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Route To"
    )
    
    class Meta:
        verbose_name = "Communication Document"
        verbose_name_plural = "Communication Documents"
    
    def __str__(self):
        return f"Document: {self.commID.title}"


class CommunicationEvent(models.Model):
    """
    Child model for Event communications
    Note: This is different from the Event model in the events app
    """
    commID = models.OneToOneField(
        Communication,
        on_delete=models.CASCADE,
        related_name='event',
        primary_key=True,
        verbose_name="Communication ID"
    )
    start_date = models.DateTimeField(verbose_name="Start Date")
    end_date = models.DateTimeField(verbose_name="End Date")
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name="Location")
    
    class Meta:
        verbose_name = "Communication Event"
        verbose_name_plural = "Communication Events"
    
    def __str__(self):
        return f"Event: {self.commID.title}"
    
    def clean(self):
        """Validate that end_date is after start_date"""
        from django.core.exceptions import ValidationError
        if self.end_date and self.start_date:
            if self.end_date < self.start_date:
                raise ValidationError("End date must be after start date.")


class ChatMessage(models.Model):
    """
    Basic chat message model to support real-time messaging.
    Conversation grouping is done via the conversation_id passed in the WebSocket URL.
    """
    conversation_id = models.CharField(max_length=255, db_index=True)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_messages'
    )
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation_id', 'created_at']),
        ]

    def __str__(self):
        return f"{self.sender} @ {self.created_at:%Y-%m-%d %H:%M}: {self.text[:30]}"

