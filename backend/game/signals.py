from uuid import UUID

from core.constants import EMPTY, PLAYER_ONE, PLAYER_TWO
from core.dataclasses import GameResult
from core.dataclasses import Status as cfs
from core.models import EloHistory, Game, Move, Player, Status
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from game.elo import EloRating as elo
from game.tasks import process_ai_move, process_game_update
from game.utils import is_board_full, is_winner


@receiver(post_save, sender=Game)
def ai_play_first_move(
    sender: Game, instance: Game, created: bool, **kwargs
) -> None:
    if created and instance.current_turn.algorithm:
        process_ai_move.delay(instance.game_id)


@receiver(post_save, sender=Move)
def update_game(sender: Move, instance: Move, created: bool, **kwargs) -> None:
    if not created and not instance.is_undone:
        return
    try:
        with transaction.atomic():
            game = Game.objects.select_for_update().get(
                game_id=UUID(str(instance.game.game_id))
            )

            update_board_and_status(game, instance)
            game.save()

            if game.current_turn.algorithm:
                process_ai_move.delay(game.game_id)

    except Exception as e:
        if not created:
            instance.delete()
        elif instance.is_undone:
            instance.is_undone = False
            instance.save()
        raise e


def update_board_and_status(game: Game, move: Move) -> None:
    token = EMPTY
    game.current_turn = move.player
    if not move.is_undone:
        token = PLAYER_ONE if move.player == game.player_one else PLAYER_TWO
        game.board[move.row][move.column] = token

        if is_winner(token, game.board, move.column, move.row):
            handle_winner(game, move.player)

        elif is_board_full(game.board):
            handle_draw(game)
        else:
            game.current_turn = get_next_turn(game, token)

        if game.status.name == cfs.CREATED.value:
            game.status = Status.objects.get(name=cfs.IN_PROGRESS.value)
            game.start_time = timezone.now()

    game.board[move.row][move.column] = token


def handle_winner(game: Game, player: Player) -> None:
    game.winner = player
    game.status = get_status_by_player(player, game)
    game.end_time = timezone.now()
    update_players_stats(game)
    process_game_update.delay(game.game_id)


def handle_draw(game: Game) -> None:
    game.status = Status.objects.get(name=cfs.DRAW.value)
    game.end_time = timezone.now()
    update_players_stats(game)
    process_game_update.delay(game.game_id)


def get_status_by_player(player: Player, game: Game) -> Status:
    return Status.objects.get(
        name=cfs.P1W.value if player == game.player_one else cfs.P2W.value
    )


def get_next_turn(game: Game, token: int) -> Player:
    return game.player_one if token == PLAYER_TWO else game.player_two


def update_players_stats(game: Game) -> None:
    player_one: Player = game.player_one
    player_two: Player = game.player_two

    match game.status.name:
        case cfs.DRAW.value:
            result = GameResult.DRAW
            player_one.draws += 1
            player_two.draws += 1
        case cfs.P1W.value:
            result = GameResult.WIN
            player_one.wins += 1
            player_two.losses += 1
        case _:
            result = GameResult.LOSS
            player_one.losses += 1
            player_two.wins += 1

    player_one.total_games += 1
    player_two.total_games += 1

    old_elo_one = player_one.elo
    old_elo_two = player_two.elo

    elo.update_player_elo(player_one, player_two, result)

    player_one.save()
    player_two.save()

    create_elo_history(player_one, game, old_elo_one)
    create_elo_history(player_two, game, old_elo_two)


def create_elo_history(player: Player, game: Game, old_elo: int) -> None:
    EloHistory.objects.create(
        player=player,
        old_elo=old_elo,
        new_elo=player.elo,
        game=game,
    )
