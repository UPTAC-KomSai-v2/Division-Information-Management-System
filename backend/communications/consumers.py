import json
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

from .models import ChatMessage


User = get_user_model()


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket consumer for real-time messaging.
    - Authenticate via JWT token supplied as query param (?token=...)
    - Room key is a string built from the two participant IDs, sorted: "<min>_<max>"
    - Only participants in the room key are allowed to connect/send
    """

    async def connect(self):
        self.room = str(self.scope["url_route"]["kwargs"]["room"])
        token = self._get_token_from_scope()

        self.user = await self._authenticate(token)
        if not self.user:
            await self.close(code=4001)
            return

        if not self._is_user_in_room(self.room, self.user.id):
            await self.close(code=4003)
            return

        self.group_name = f"chat_{self.room}"
        self.user_group = f"user_{self.user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        # Join a per-user group so we can broadcast deletions even when not in this room
        await self.channel_layer.group_add(self.user_group, self.channel_name)
        await self.accept()

        # send recent history
        history = await self._get_recent_messages()
        for msg in history:
            await self.send_json(self._serialize_message(msg))

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
        if hasattr(self, "user_group"):
            await self.channel_layer.group_discard(self.user_group, self.channel_name)

    async def receive_json(self, content, **kwargs):
        text = (content.get("text") or "").strip()
        if not text or not getattr(self, "user", None):
            return

        if not self._is_user_in_room(self.room, self.user.id):
            await self.close(code=4003)
            return

        message = await self._create_message(text)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "payload": self._serialize_message(message),
            },
        )

    async def chat_message(self, event):
        await self.send_json(event["payload"])

    async def chat_deletion(self, event):
        # Broadcast deletion event to clients in the room
        await self.send_json(event["payload"])

    # Helpers
    def _get_token_from_scope(self):
        query_string = self.scope.get("query_string", b"").decode()
        params = parse_qs(query_string)
        tokens = params.get("token", [])
        return tokens[0] if tokens else None

    @database_sync_to_async
    def _authenticate(self, raw_token):
        if not raw_token:
            return None
        jwt_auth = JWTAuthentication()
        try:
            validated = jwt_auth.get_validated_token(raw_token)
            return jwt_auth.get_user(validated)
        except (InvalidToken, AuthenticationFailed):
            return None

    def _is_user_in_room(self, room_key, user_id):
        try:
            parts = room_key.split("_")
            ints = {int(p) for p in parts}
            return user_id in ints
        except Exception:
            return False

    @database_sync_to_async
    def _create_message(self, text):
        return ChatMessage.objects.create(
            conversation_id=self.room,
            sender=self.user,
            text=text,
            created_at=timezone.now(),
        )

    @database_sync_to_async
    def _get_recent_messages(self, limit=30):
        return list(
            ChatMessage.objects.filter(conversation_id=self.room)
            .select_related("sender")
            .order_by("-created_at")[:limit][::-1]
        )

    def _serialize_message(self, msg):
        return {
            "id": msg.id,
            "conversation_id": msg.conversation_id,
            "text": msg.text,
            "sender_id": msg.sender_id,
            "sender_name": getattr(msg.sender, "email", str(msg.sender)),
            "created_at": msg.created_at.isoformat(),
        }
