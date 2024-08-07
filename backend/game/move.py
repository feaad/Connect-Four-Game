import contextlib
from typing import Optional, Tuple

from ai.algorithm.alphabeta import AlphaBeta
from ai.algorithm.minimax import Minimax
from asgiref.sync import sync_to_async
from core.constants import PLAYER_ONE, PLAYER_TWO
from core.dataclasses import Algorithm as cfa
from core.dataclasses import Status as cfs
from core.models import Game, Move, Player

from game import utils


def get_game_status(game_id: str) -> Optional[str]:
    with contextlib.suppress(Game.DoesNotExist):
        game = Game.objects.get(game_id=game_id)

        return game.status.name

    return None


def compute_ai_move(game_id) -> Optional[Tuple[int, int, int]]:
    with contextlib.suppress(Game.DoesNotExist):
        game = Game.objects.get(game_id=game_id)

        if game.current_turn.algorithm is None:
            return

        current_turn = game.current_turn.algorithm.code_name

        player = (
            PLAYER_ONE if game.current_turn == game.player_one else PLAYER_TWO
        )

        match current_turn:
            case cfa.MINIMAX.value:
                algorithm = Minimax(player, game.board, game.depth)
            case cfa.ALPHA_BETA.value:
                algorithm = AlphaBeta(player, game.board, game.depth)
            case _:
                return
        row, column = algorithm.get_move()

        Move.objects.create(
            game=game,
            player=game.current_turn,
            row=row,
            column=column,
        )

        return player, row, column
    raise ValueError("Game does not exist")


async def play_move(
    game_id: str, player: Player, row: int, column: int
) -> bool:
    with contextlib.suppress(Game.DoesNotExist):
        game = await sync_to_async(Game.objects.get)(game_id=game_id)

        status_name = await sync_to_async(lambda: game.status.name)()

        if status_name not in [cfs.IN_PROGRESS.value, cfs.CREATED.value]:
            raise ValueError("Game is not in progress")

        current_turn = await sync_to_async(lambda: game.current_turn)()
        if current_turn != player:
            raise ValueError("It is not your turn")

        columns = await sync_to_async(lambda: game.columns)()
        rows = await sync_to_async(lambda: game.rows)()
        if not (0 <= column < columns and 0 <= row < rows):
            raise ValueError(
                f"(Column,Row) must be 0 or less than ({columns},{rows})"
            )

        board = await sync_to_async(lambda: game.board)()
        if not utils.is_valid_move(board, column, row):
            raise ValueError("Invalid move")

        await sync_to_async(Move.objects.create)(
            game=game,
            player=player,
            row=row,
            column=column,
        )
        return True

    raise ValueError("Game does not exist")


async def undo_move(game_id: str, player: Player) -> Optional[Tuple[int, int]]:
    with contextlib.suppress(Move.DoesNotExist):
        move: Move = await sync_to_async(
            Move.objects.filter(
                game_id=game_id, player=player, is_undone=False
            ).latest
        )("created_at")

        if not await sync_to_async(utils.can_undo_move)(move):
            raise ValueError("You cannot undo this move")

        column = await sync_to_async(lambda: move.column)()
        row = await sync_to_async(lambda: move.row)()

        move.is_undone = True
        await sync_to_async(move.save)()

        return row, column

    raise ValueError("No moves to undo")
