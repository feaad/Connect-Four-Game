from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from core.constants import MATCHMAKING_QUEUE
from core.redis import redis_client

from game.match_making import find_match_for_player, notify_players
from game.move import compute_ai_move, get_game_status


@shared_task(name="game.tasks.process_matchmaking")
def process_matchmaking():
    run = 0
    message = "Matchmaking complete"

    while True:
        player_ids = redis_client.zrange(
            MATCHMAKING_QUEUE, 0, 0, withscores=False
        )
        if not player_ids:
            break

        player_id = player_ids[0]

        if game := find_match_for_player(player_id):
            run = 2
            notify_players(game)

        run = 1 if run == 0 else run

    match run:
        case 0:
            message = "No players in the queue"
        case 1:
            message = "Matchmaking Completed"
        case 2:
            message = "Matches Found"

    return message


@shared_task(
    name="game.tasks.compute_ai_move",
)
def process_ai_move(game_id):
    if position := compute_ai_move(game_id):
        player, row, column = position
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"game_{game_id}",
            {
                "type": "ai_move",
                "message": {
                    "player": player,
                    "row": row,
                    "column": column,
                },
            },
        )


@shared_task(name="game.tasks.game_update")
def process_game_update(game_id):
    if status := get_game_status(game_id):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"game_{game_id}",
            {
                "type": "game_update",
                "message": {"status": status},
            },
        )
