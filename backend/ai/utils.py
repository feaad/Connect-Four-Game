from math import inf
from typing import List, Tuple

import numpy as np
import numpy.typing as npt
from ai.board import Board
from core.constants import EMPTY, PLAYER_ONE, PLAYER_TWO


def get_score(board: npt.NDArray[np.int32], player: int) -> int:
    score = 0

    score += _centre_score(board, player)
    score += _horizontal_score(board, player)
    score += _vertical_score(board, player)
    score += _diagonal_score(board, player)

    return score


def _evaluate_sliding_window(window: List[int], player: int) -> int:
    score = 0
    opponent = PLAYER_ONE if player == PLAYER_TWO else PLAYER_TWO

    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opponent) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def _centre_score(board: npt.NDArray[np.int32], player: int) -> int:
    cols = board.shape[1] // 2

    centre_array = [int(i) for i in list(board[:, cols])]
    centre_count = centre_array.count(player)

    return centre_count * 3


def _horizontal_score(board: npt.NDArray[np.int32], player: int) -> int:
    score = 0

    for r in range(board.shape[0]):
        row = [int(i) for i in list(board[r, :])]
        for c in range(board.shape[1] - 3):
            window = row[c : c + 4]
            score += _evaluate_sliding_window(window, player)

    return score


def _vertical_score(board: npt.NDArray[np.int32], player: int) -> int:
    score = 0

    for c in range(board.shape[1]):
        col = [int(i) for i in list(board[:, c])]
        for r in range(board.shape[0] - 3):
            window = col[r : r + 4]
            score += _evaluate_sliding_window(window, player)

    return score


def _diagonal_score(board: npt.NDArray[np.int32], player: int) -> int:
    score = 0

    # Positive Slope Diagonals
    for r in range(board.shape[0] - 3):
        for c in range(board.shape[1] - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += _evaluate_sliding_window(window, player)

    # Negative Slope Diagonals
    for r in range(board.shape[0] - 3):
        for c in range(board.shape[1] - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += _evaluate_sliding_window(window, player)

    return score


def evaluate_board(board: Board, player: int) -> Tuple[int, float]:
    opponent = PLAYER_ONE if player == PLAYER_TWO else PLAYER_TWO

    if not board.game_over():
        return -1, get_score(board.board, player)

    if board.is_winner(player):
        return -1, inf
    elif board.is_winner(opponent):
        return -1, -inf
    else:
        return -1, 0
