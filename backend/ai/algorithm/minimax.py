from math import inf
from random import choice
from typing import List, Tuple

from ai.board import Board
from ai.utils import evaluate_board
from core.constants import MM_DEPTH
from core.dataclasses import Algorithm as cfa

from .algorithm import Algorithm


class Minimax(Algorithm):
    def __init__(self, player: int, board: List[List[int]]) -> None:
        super().__init__(player, board)
        self.name = cfa.MINIMAX.value

    def get_move(self) -> Tuple[int, int]:
        column, _ = self._minimax(self.board, MM_DEPTH)
        row = self.board.get_open_row(column)

        return row, column

    def _minimax(
        self, board: Board, depth: int, is_maximizing: bool = True
    ) -> Tuple[int, float]:
        if depth == 0 or board.game_over():
            return evaluate_board(board, self.player)

        open_columns = board.get_open_columns()
        best_column = choice(open_columns)
        best_score = -inf if is_maximizing else inf
        player = self.player if is_maximizing else self.opponent

        for column in open_columns:
            board.drop_token(column, player)
            _, score = self._minimax(board, depth - 1, not is_maximizing)
            board.undo_move()

            if (is_maximizing and score > best_score) or (
                not is_maximizing and score < best_score
            ):
                best_column = column
                best_score = score

        return best_column, best_score
