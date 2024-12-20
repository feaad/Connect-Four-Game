from math import inf
from random import choice
from typing import List, Tuple

from ai.board import Board
from ai.utils import evaluate_board
from core.dataclasses import Algorithm as cfa

from .algorithm import Algorithm

ALPHA = -inf
BETA = inf


class AlphaBeta(Algorithm):
    def __init__(self, player: int, board: List[List[int]], depth) -> None:
        super().__init__(player, board, depth)
        self.name = cfa.ALPHA_BETA.value

    def get_move(self) -> Tuple[int, int]:
        column, _ = self._alpha_beta(self.board, self.depth, ALPHA, BETA)
        row = self.board.get_open_row(column)

        return row, column

    def _alpha_beta(
        self,
        board: Board,
        depth: int,
        alpha: float,
        beta: float,
        is_maximizing: bool = True,
    ) -> Tuple[int, float]:
        if depth == 0 or board.game_over():
            return evaluate_board(board, self.player)

        open_columns = board.get_open_columns()
        best_column = choice(open_columns)
        best_score = -inf if is_maximizing else inf
        player = self.player if is_maximizing else self.opponent

        for column in open_columns:
            board.drop_token(column, player)

            _, score = self._alpha_beta(
                board, depth - 1, alpha, beta, not is_maximizing
            )

            board.undo_move()

            if (
                is_maximizing
                and score > best_score
                or not is_maximizing
                and score < best_score
            ):
                best_score = score
                best_column = column

            if is_maximizing:
                alpha = max(alpha, best_score)
            else:
                beta = min(beta, best_score)

            if alpha >= beta:
                break

        return best_column, best_score
