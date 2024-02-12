from board.board import Board
from board.colour import Colour

from .algorithm import Algorithm

from typing import Tuple

# TODO: Put in a configuration file
DEPTH = 4


class MinMax(Algorithm):
    def __init__(self, colour: Colour) -> None:
        super().__init__(colour)
    
    def min_max(self, board: Board, depth: int, is_maximizing: bool = True)  -> Tuple[int, float]:

        # if depth = 0 or node is a terminal node then
        #     return the heuristic value of node
        # if maximizingPlayer then
        #     value := −∞
        #     for each child of node do
        #         value := max(value, minimax(child, depth − 1, FALSE))
        #     return value
        # else (* minimizing player *)
        #     value := +∞
        #     for each child of node do
        #         value := min(value, minimax(child, depth − 1, TRUE))
        #     return value

    def get_best_move(self, board: Board) -> int:
        return self.min_max(board, DEPTH)
