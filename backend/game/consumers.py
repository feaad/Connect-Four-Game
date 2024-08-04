import json

from channels.db import database_sync_to_async
from core.constants import PLAYER_ONE, PLAYER_TWO
from core.consumers import CLOSE_CODE, BaseConsumer
from core.models import Game
from game import move


class GameConsumer(BaseConsumer):
    async def setup(self) -> None:
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.group_name = f"game_{self.game_id}"

        try:
            game = await database_sync_to_async(Game.objects.get)(
                game_id=self.game_id
            )
        except Game.DoesNotExist:
            await self.close(code=CLOSE_CODE, reason="Game does not exist")
            return

        if not await self.is_player_in_game(game):
            await self.close(code=CLOSE_CODE, reason="User is not in the game")
            return

        self.token = (
            PLAYER_ONE if self.player == game.player_one else PLAYER_TWO
        )
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    @database_sync_to_async
    def is_player_in_game(self, game: Game) -> bool:
        return game.player_one == self.player or game.player_two == self.player

    async def player_move(self, data: dict) -> None:
        try:
            row, column = data["row"], data["column"]
            success = await move.play_move(
                self.game_id, self.player, row, column
            )

            if success:
                await self.broadcast_message(
                    "player_move",
                    {"row": row, "column": column},
                )
        except ValueError as e:
            await self.send_error(str(e))

    async def undo_move(self, _: dict) -> None:
        try:
            if position := await move.undo_move(self.game_id, self.player):
                row, column = position
                await self.broadcast_message(
                    "undo_move",
                    {"row": row, "column": column},
                )
        except ValueError as e:
            await self.send_error(str(e))

    async def broadcast_message(self, event_type: str, message: dict) -> None:
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "game_notification",
                "event_type": event_type,
                "player_token": self.token,
                "message": message,
            },
        )

    async def game_notification(self, event: dict) -> None:
        await self.send(
            text_data=json.dumps(
                {
                    "event_type": event["event_type"],
                    "player_token": event["player_token"],
                    "message": event["message"],
                }
            )
        )

    async def ai_move(self, data: dict) -> None:
        await self.send(text_data=json.dumps({"message": data["message"]}))

    async def game_update(self, data: dict) -> None:
        await self.send(text_data=json.dumps({"message": data["message"]}))
