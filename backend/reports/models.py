from django.db import models
from django.conf import settings
from django.utils import timezone


class FacultyActivity(models.Model):
    """
    Tracks faculty activity metrics for reporting.
    This can be populated from various sources (documents, events, etc.)
    """
    faculty = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='faculty_activities'
    )
    unit = models.CharField(max_length=255, help_text="Department/Unit name")
    
    # Activity metrics
    publications_count = models.IntegerField(default=0, help_text="Number of publications")
    service_hours = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0,
        help_text="Total service hours"
    )
    trainings_attended = models.IntegerField(default=0, help_text="Number of trainings attended")
    
    # Period for which this activity is recorded
    period_start = models.DateField(help_text="Start date of the activity period")
    period_end = models.DateField(help_text="End date of the activity period")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Faculty Activities"
        ordering = ['-period_end', 'faculty']
        indexes = [
            models.Index(fields=['faculty', 'period_start', 'period_end']),
            models.Index(fields=['unit']),
        ]
    
    def __str__(self):
        return f"{self.faculty.get_full_name()} - {self.unit} ({self.period_start} to {self.period_end})"


class Report(models.Model):
    """
    Stores generated reports metadata
    """
    report_type = models.CharField(max_length=100, default='FACULTY_ACTIVITY')
    title = models.CharField(max_length=255)
    date_from = models.DateField()
    date_to = models.DateField()
    unit_filter = models.CharField(max_length=255, blank=True, null=True, help_text="Filter by unit/event type")
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='generated_reports'
    )
    generated_at = models.DateTimeField(auto_now_add=True)
    
    # Store report data as JSON (optional, for caching)
    report_data = models.JSONField(blank=True, null=True, help_text="Cached report data")
    
    class Meta:
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['-generated_at']),
            models.Index(fields=['report_type']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.date_from} to {self.date_to}"

