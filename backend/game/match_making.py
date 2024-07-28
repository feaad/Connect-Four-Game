import contextlib
from typing import Optional
from uuid import UUID

from core.constants import MATCHMAKING_QUEUE
from core.models import Game, MatchMakingQueue, Player, Status
from core.redis import redis_client
from core.dataclasses import Status as cfs


def add_player_to_queue(player_id, elo_rating) -> UUID:
    redis_client.zadd(MATCHMAKING_QUEUE, {str(player_id): elo_rating})

    match = MatchMakingQueue.objects.create(
        player_id=player_id, status=Status.objects.get(name=cfs.QUEUED)
    )

    return match.queue_id


def remove_player_from_queue(player_id, game: Optional[Game] = None) -> int:
    status = 0
    with contextlib.suppress(MatchMakingQueue.DoesNotExist):
        match = MatchMakingQueue.objects.get(
            player=player_id, status=Status.objects.get(name=cfs.QUEUED)
        )

        if game:
            match.status = Status.objects.get(name=cfs.MATCHED)
            match.game = game
            status = 1
        else:
            match.status = Status.objects.get(name=cfs.CANCELLED)
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
    # Send a notification to both players
    # TODO: Implement this
    print(f"Game {game.game_id} has been created")
    print(f"Player 1: {game.player_one.player_id}")
    print(f"Player 2: {game.player_two.player_id}")
