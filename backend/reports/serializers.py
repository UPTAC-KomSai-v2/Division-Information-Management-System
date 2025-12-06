from rest_framework import serializers
from .models import Report, FacultyActivity
from accounts.serializers import UserListSerializer


class FacultyActivitySerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.get_full_name', read_only=True)
    faculty_email = serializers.EmailField(source='faculty.email', read_only=True)
    
    class Meta:
        model = FacultyActivity
        fields = [
            'id',
            'faculty',
            'faculty_name',
            'faculty_email',
            'unit',
            'publications_count',
            'service_hours',
            'trainings_attended',
            'period_start',
            'period_end',
            'created_at',
            'updated_at',
        ]


class ReportSerializer(serializers.ModelSerializer):
    generated_by_email = serializers.EmailField(source='generated_by.email', read_only=True)
    
    class Meta:
        model = Report
        fields = [
            'id',
            'report_type',
            'title',
            'date_from',
            'date_to',
            'unit_filter',
            'generated_by',
            'generated_by_email',
            'generated_at',
            'report_data',
        ]
        read_only_fields = ['generated_by', 'generated_at']


class ReportGenerateSerializer(serializers.Serializer):
    """Serializer for report generation request"""
    date_from = serializers.DateField(required=True)
    date_to = serializers.DateField(required=True)
    unit = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    title = serializers.CharField(required=False, allow_blank=True)


class ReportDataSerializer(serializers.Serializer):
    """Serializer for report data rows"""
    facultyName = serializers.CharField()
    unit = serializers.CharField()
    publications = serializers.IntegerField()
    serviceHours = serializers.DecimalField(max_digits=10, decimal_places=2)
    trainingsAttended = serializers.IntegerField()

