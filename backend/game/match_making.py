import contextlib
from typing import Optional
from uuid import UUID

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from core.constants import MATCHMAKING_QUEUE
from core.dataclasses import Status as cfs
from core.models import Game, MatchMakingQueue, Player, Status
from core.redis import redis_client
from core.utils import get_username_or_name

NOTIFICATION_TYPE = "matchmaking"


def add_player_to_queue(player_id, elo_rating) -> UUID:
    redis_client.zadd(MATCHMAKING_QUEUE, {str(player_id): elo_rating})

    match = MatchMakingQueue.objects.create(
        player_id=player_id, status=Status.objects.get(name=cfs.QUEUED.value)
    )

    return match.queue_id


def remove_player_from_queue(player_id, game: Optional[Game] = None) -> int:
    status = 0
    with contextlib.suppress(MatchMakingQueue.DoesNotExist):
        match = MatchMakingQueue.objects.get(
            player=player_id, status=Status.objects.get(name=cfs.QUEUED.value)
        )

        if game:
            match.status = Status.objects.get(name=cfs.MATCHED.value)
            match.game = game
            status = 1
        else:
            match.status = Status.objects.get(name=cfs.CANCELLED.value)
            status = 2

        match.save()

        redis_client.zrem(MATCHMAKING_QUEUE, player_id)

    return status


def find_match_for_player(player_id) -> Game | None:
    with contextlib.suppress(Player.DoesNotExist):
        player_data = Player.objects.get(player_id=player_id)
        player_rating = player_data.elo

        # Get players from the queue with Elo ratings
        players = redis_client.zrangebyscore(
            MATCHMAKING_QUEUE, "-inf", "+inf", withscores=True
        )
        potential_opponents = [
            (pid, score) for pid, score in players if pid != player_id
        ]

        if not potential_opponents:
            return None

        # Match based on closest rating
        opponent_id, _ = min(
            potential_opponents, key=lambda x: abs(x[1] - player_rating)
        )

        game = create_game(player_id, opponent_id)

        # Remove both players from the queue
        remove_player_from_queue(player_id, game)
        remove_player_from_queue(opponent_id, game)

        return game

    redis_client.zrem(MATCHMAKING_QUEUE, player_id)
    return None


def create_game(player1_id, player2_id):
    # Create a game instance
    return Game.objects.create(
        player_one=Player.objects.get(player_id=player1_id),
        player_two=Player.objects.get(player_id=player2_id),
        status=Status.objects.get(name=cfs.CREATED),
        current_turn=Player.objects.get(player_id=player1_id),
    )


def notify_players(game: Game):
    game_id = game.game_id
    p1_id = game.player_one.player_id
    p2_id = game.player_two.player_id

    p1_name = get_username_or_name(game.player_one)
    p2_name = get_username_or_name(game.player_two)

    channel_layer = get_channel_layer()

    send_notification(channel_layer, p1_id, game_id, p1_name, p2_name)
    send_notification(channel_layer, p2_id, game_id, p1_name, p2_name)


def send_notification(channel_layer, player_id, game_id, p1_name, p2_name):
    async_to_sync(channel_layer.group_send)(
        f"player_{player_id}",
        {
            "type": NOTIFICATION_TYPE,
            "message": {
                "game_id": str(game_id),
                "player_one": p1_name,
                "player_two": p2_name,
            },
        },
    )
