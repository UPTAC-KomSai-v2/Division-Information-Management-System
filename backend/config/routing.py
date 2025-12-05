from django.urls import path

from communications.consumers import ChatConsumer

websocket_urlpatterns = [
    # room is a string key built from the two participant IDs (e.g., "1_7")
    path("ws/messages/<str:room>/", ChatConsumer.as_asgi()),
]
