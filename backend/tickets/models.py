from django.db import models
from django.conf import settings
from django.db.models import Max


class Ticket(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        RESOLVED = "RESOLVED", "Resolved"
        CLOSED = "CLOSED", "Closed"

    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        URGENT = "URGENT", "Urgent"

    ticket_id = models.CharField(max_length=20, unique=True, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tickets'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='assigned_tickets',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['ticket_id']),
        ]

    def __str__(self):
        return f"{self.ticket_id} - {self.title}"

    def save(self, *args, **kwargs):
        """Auto-generate ticket_id if not set"""
        if not self.ticket_id:
            self.ticket_id = self.generate_ticket_id()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_ticket_id():
        """Generate unique ticket ID in format TCK-001, TCK-002, etc."""
        # Get the highest ticket number
        last_ticket = Ticket.objects.aggregate(Max('ticket_id'))
        last_id = last_ticket.get('ticket_id__max', None)
        
        if last_id:
            # Extract the number part (e.g., "TCK-001" -> 1)
            try:
                last_num = int(last_id.split('-')[1])
                new_num = last_num + 1
            except (IndexError, ValueError):
                new_num = 1
        else:
            new_num = 1
        
        # Format as TCK-XXX with leading zeros
        return f"TCK-{new_num:03d}"

    @property
    def creator_email(self):
        """Get creator's email"""
        return self.created_by.email if self.created_by else ""

    @property
    def assignee_email(self):
        """Get assignee's email"""
        return self.assigned_to.email if self.assigned_to else None
