from rest_framework.routers import DefaultRouter
from .views import CommunicationViewSet

router = DefaultRouter()
router.register(r'communications', CommunicationViewSet, basename='communication')

urlpatterns = router.urls

