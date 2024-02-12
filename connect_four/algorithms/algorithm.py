from typing import List

from board.board import Board
from board.colour import Colour

WINDOW_SIZE = 4

class Algorithm:
    
    colour: Colour
    opponent: Colour

    def __init__(self, colour: Colour) -> None:
        self.colour = colour
        self.opponent = Colour.YELLOW if colour == Colour.RED else Colour.RED
    
    
    def get_best_move(self, board: Board) -> int:
        raise NotImplementedError(
            "Algorithm.get_best_move() must be implemented to return a move."
        )

    def get_score(self, board: Board, colour: Colour) -> int:
        score: int = 0
        score += self.__centre_score(board, colour)
        score += self.__horizontal_score(board, colour)
        score += self.__vertical_score(board, colour)
        score += self.__diagonal_score(board, colour)

        return score

    def __evaluate_sliding_window(self, sliding_window: List[int], colour: Colour) -> int:
        score: int = 0

        return score

    def __centre_score(self, board: Board, colour: Colour) -> int:
        score: int = 0

        return score

    def __horizontal_score(self, board: Board, colour: Colour) -> int:
        score: int = 0

        return score

    def __vertical_score(self, board: Board, colour: Colour) -> int:
        score: int = 0

        return score

    def __diagonal_score(self, board: Board, colour: Colour) -> int:
        score: int = 0

        return score