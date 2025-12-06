from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import CommunicationViewSet, ChatHistoryView

router = DefaultRouter()
router.register(r'communications', CommunicationViewSet, basename='communication')

urlpatterns = router.urls + [
    path('chat/<str:room>/delete/', ChatHistoryView.as_view(), name='chat-delete'),
]

