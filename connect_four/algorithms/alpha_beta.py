import copy
from random import choice
from typing import List, Tuple

from board.board import Board
from board.colour import Colour

from .algorithm import Algorithm

# TODO: Create a configuration file for these constants
DEPTH = 6

ALPHA = float("-inf")
BETA = float("inf")


class AlphaBeta(Algorithm):
    def __init__(self, colour: Colour) -> None:
        super().__init__(colour)

    def alpha_beta(
        self,
        board: Board,
        depth: int,
        alpha: float,
        beta: float,
        is_maximizing: bool = True,
    ) -> Tuple[int, float]:
        if depth == 0 or board.is_game_over():
            return self.evaluate(board)

        empty_cols: List[int] = board.get_open_columns()
        best_col = choice(empty_cols)
        best_score = float("-inf") if is_maximizing else float("inf")

        for col in empty_cols:
            temp_board = copy.deepcopy(board)
            temp_board.drop_token(col, self.colour if is_maximizing else self.opponent)

            _, score = self.alpha_beta(
                temp_board, depth - 1, alpha, beta, not is_maximizing
            )

            if (is_maximizing and score > best_score) or (
                not is_maximizing and score < best_score
            ):
                best_col = col
                best_score = score


            if is_maximizing:
                alpha = max(alpha, best_score)
            else:
                beta = min(beta, best_score)

            if alpha >= beta:
                break

        return best_col, best_score

    def get_best_move(self, board: Board) -> int:
        col, _ = self.alpha_beta(board, DEPTH, ALPHA, BETA)

        # TODO: Clean the .value.symbol
        print(
            f"{self.colour.value.symbol} AI-Alpha, kindly enter the column number: {col+1}"
        )

        return col
