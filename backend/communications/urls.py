from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import CommunicationViewSet, ChatHistoryView, PresenceOfflineView, PresenceOnlineView

router = DefaultRouter()
router.register(r'communications', CommunicationViewSet, basename='communication')

urlpatterns = router.urls + [
    path('chat/<str:room>/delete/', ChatHistoryView.as_view(), name='chat-delete'),
    path('presence/offline/', PresenceOfflineView.as_view(), name='presence-offline'),
    path('presence/online/', PresenceOnlineView.as_view(), name='presence-online'),
]

