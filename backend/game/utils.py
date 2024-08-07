from typing import List, Optional

from core.constants import CONNECT, EMPTY, K_DEPTH
from core.dataclasses import Status as cfs
from core.models import Move, Player


def is_valid_move(board: List[List[int]], column: int, row: int) -> bool:
    """
    Check if the move is valid.

    Parameters
    ----------
    board : List[List[int]]
        The game board.

    column : int
        The column to move.

    row : int
        The row to move.

    Returns
    -------
    bool
        True if the move is valid, False otherwise.

    """
    if column < 0 or column >= len(board[0]):
        return False
    if row < 0 or row >= len(board):
        return False
    if board[row][column] != EMPTY:
        return False

    if row < len(board) - 1 and board[row + 1][column] == EMPTY:
        return False

    return True


def is_board_full(board: List[List[int]]) -> bool:
    """
    Check if the board is full.

    Parameters
    ----------
    board : List[List[int]]
        The game board.

    Returns
    -------
    bool
        True if the board is full, False otherwise.

    """
    return all(EMPTY not in row for row in board)


def can_undo_move(move: Move) -> bool:
    """
    Check if the player can undo the last move.

    Parameters
    ----------
    game : Game
        The game instance.

    Returns
    -------
    bool
        True if the player can undo the last move, False otherwise.

    """
    game = move.game

    if game.status.name not in [cfs.IN_PROGRESS.value, cfs.CREATED.value]:
        return False

    last_move = (
        Move.objects.filter(game=game, is_undone=False)
        .order_by("-created_at")
        .first()
    )

    if last_move != move:
        return False

    return True


def is_winner(
    token: int, board: List[List[int]], column: int, row: int
) -> bool:
    if _check_horizontal_win(token, board, row):
        return True

    if _check_vertical_win(token, board, column):
        return True

    if _check_diagonal_win(token, board, column, row):
        return True

    return False


def _check_horizontal_win(
    token: int, board: List[List[int]], row: int
) -> bool:
    consecutive_tokens = 0
    for cell in board[row]:
        if cell == token:
            consecutive_tokens += 1
            if consecutive_tokens == CONNECT:
                return True
        else:
            consecutive_tokens = 0

    return False


def _check_vertical_win(
    token: int, board: List[List[int]], column: int
) -> bool:
    consecutive_tokens = 0
    for row in board:
        if row[column] == token:
            consecutive_tokens += 1
            if consecutive_tokens == CONNECT:
                return True
        else:
            consecutive_tokens = 0

    return False


def _check_diagonal_win(
    token: int, board: List[List[int]], column: int, row: int
) -> bool:
    directions = [(1, 1), (1, -1)]
    width = len(board[0])
    height = len(board)

    for dx, dy in directions:
        consecutive_tokens = 1

        for direction in [-1, 1]:
            for d in range(1, CONNECT):
                x = column + direction * d * dx
                y = row + direction * d * dy

                if 0 <= x < width and 0 <= y < height and board[y][x] == token:
                    consecutive_tokens += 1
                else:
                    break

                if consecutive_tokens >= CONNECT:
                    return True

    return False


def compute_depth(
    difficulty_level: int, player_one: Player, player_two: Player
) -> Optional[int]:
    if player_one.algorithm:
        algo_depth = player_one.algorithm.depth
        elo = player_two.elo
    else:
        algo_depth = player_two.algorithm.depth
        elo = player_one.elo

    if not algo_depth:
        return None

    min_elo = Player.objects.filter(is_human=True).order_by("elo").first().elo
    max_elo = Player.objects.filter(is_human=True).order_by("elo").last().elo

    norm_elo = (
        (elo - min_elo) / (max_elo - min_elo) if max_elo != min_elo else 0
    )

    depth = (2 * difficulty_level) + algo_depth + (K_DEPTH * norm_elo)

    return round(depth)
