from celery import shared_task
from celery.utils.log import get_task_logger
from core.constants import MATCHMAKING_QUEUE
from core.redis import redis_client
from game.match_making import find_match_for_player, notify_players

logger = get_task_logger(__name__)


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
