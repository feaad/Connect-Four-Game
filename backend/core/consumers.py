import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from core.models import Player
from core.utils import get_player

CLOSE_CODE = 1008


class BaseConsumer(AsyncWebsocketConsumer):
    group_name: str = "base"

    async def connect(self) -> None:
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close(
                code=CLOSE_CODE, reason="User is not authenticated"
            )
            return

        self.player: Player = await database_sync_to_async(get_player)(
            self.user
        )
        if self.player is None:
            await self.close(code=CLOSE_CODE, reason="User does not exist")
            return

        await self.setup()

    async def setup(self) -> None:
        raise NotImplementedError("Setup method not implemented")

    async def disconnect(self, close_code: int) -> None:
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )

    async def receive(self, text_data: str) -> None:
        data = json.loads(text_data)
        event_type = data.get("type")

        if handler := getattr(self, f"{event_type}", None):
            await handler(data)

    async def send_error(self, message: str) -> None:
        await self.send(
            text_data=json.dumps({"type": "error", "message": message})
        )

    async def broadcast_message(self, event_type: str, message: dict) -> None:
        raise NotImplementedError("Broadcast Message method not implemented")
