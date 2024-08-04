import json

from channels.db import database_sync_to_async
from core.consumers import CLOSE_CODE, BaseConsumer
from django.utils import timezone


class PlayerConsumer(BaseConsumer):
    async def setup(self) -> None:
        self.player_id = self.scope["url_route"]["kwargs"]["player_id"]
        self.group_name = f"player_{self.player_id}"

        if self.player.player_id != self.player_id:
            await self.close(
                code=CLOSE_CODE, reason="Player ID does not match"
            )
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def matchmaking(self, data: dict) -> None:
        await self.send(text_data=json.dumps({"message": data["message"]}))

    async def notification(self, data: dict) -> None:
        await self.send(text_data=json.dumps({"message": data}))

    async def ping(self, _: dict) -> None:
        self.player.last_activity = timezone.now()
        await database_sync_to_async(self.player.save)()
