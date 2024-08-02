from ai.board import Board
from core.constants import PLAYER_ONE, PLAYER_TWO


class Algorithm:
    def __init__(self, player: int, board: Board) -> None:
        self.name = "Algorithm"
        self.player = player
        self.opponent = PLAYER_ONE if player == PLAYER_TWO else PLAYER_TWO
        self.board = board

    def get_move(self) -> int:
        raise NotImplementedError(
            "Algorithm.get_move() must be implemented in subclass"
        )
