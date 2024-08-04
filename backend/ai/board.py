from itertools import product
from typing import List, Tuple

import numpy as np
import numpy.typing as npt
from core.constants import EMPTY, PLAYER_ONE, PLAYER_TWO


class Board:
    def __init__(self, board: npt.NDArray[np.int32], player: int) -> None:
        self.board = board
        self.player = player
        self.opponent = PLAYER_ONE if player == PLAYER_TWO else PLAYER_TWO

        self.rows = board.shape[0]
        self.columns = board.shape[1]

        self.moves: List[Tuple[int, int]] = []

    def game_over(self) -> bool:
        return (
            self.is_full()
            or self.is_winner(self.player)
            or self.is_winner(self.opponent)
        )

    def is_full(self) -> bool:
        return bool(np.all(self.board != EMPTY))

    def is_winner(self, token: int) -> bool:
        for r, c in product(range(self.rows), range(self.columns - 3)):
            if np.all(self.board[r, c : c + 4] == token):
                return True

        for r, c in product(range(self.rows - 3), range(self.columns)):
            if np.all(self.board[r : r + 4, c] == token):
                return True

        for r, c in product(range(self.rows - 3), range(self.columns - 3)):
            if np.all([self.board[r + i, c + i] == token for i in range(4)]):
                return True

        return any(
            np.all([self.board[r - i, c + i] == token for i in range(4)])
            for r, c in product(range(3, self.rows), range(self.columns - 3))
        )

    def drop_token(self, column: int, token: int) -> bool:
        if not 0 <= column < self.columns:
            return False

        empty_rows = np.where(self.board[:, column] == EMPTY)[0]

        if empty_rows.size > 0:
            row = empty_rows[-1]

            self.board[row, column] = token
            self.moves.append((row, column))

            return True

        return False

    def undo_move(self) -> bool:
        if not self.moves:
            return False

        row, column = self.moves.pop()
        self.board[row, column] = EMPTY

        return True

    def get_open_columns(self) -> List[int]:
        open_columns = np.where(self.board[0] == EMPTY)[0]

        return open_columns.tolist()

    def get_open_row(self, column: int) -> int:
        empty_rows = np.where(self.board[:, column] == EMPTY)[0]

        return int(empty_rows[-1]) if empty_rows.size > 0 else -1

    @property
    def raw(self) -> List[List[int]]:
        return self.board.tolist()
