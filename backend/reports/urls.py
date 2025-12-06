from rest_framework.routers import DefaultRouter
from .views import ReportViewSet, FacultyActivityViewSet

router = DefaultRouter()
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'faculty-activities', FacultyActivityViewSet, basename='faculty-activity')

urlpatterns = router.urls

