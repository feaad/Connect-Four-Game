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
    
    def evaluate(self, board: Board) -> int:
        if board.is_game_over():
            if board.is_winner(self.colour):
                return -1, float("inf")
            elif board.is_winner(self.opponent):
                return -1, float("-inf")
            else:
                return -1, 0
        else:
            return -1, self.get_score(board, self.colour)

    def get_score(self, board: Board, colour: Colour) -> int:
        score: int = 0
        score += self.__centre_score(board, colour)
        score += self.__horizontal_score(board, colour)
        score += self.__vertical_score(board, colour)
        score += self.__diagonal_score(board, colour)

        return score

    def __evaluate_sliding_window(
        self, sliding_window: List[int], colour: Colour
    ) -> int:
        score: int = 0
        # TODO: Tune these values

        if sliding_window.count(colour) == 4:
            score += 100
        elif (
            sliding_window.count(colour) == 3 and sliding_window.count(Colour.GRAY) == 1
        ):
            score += 5
        elif (
            sliding_window.count(colour) == 2 and sliding_window.count(Colour.GRAY) == 2
        ):
            score += 2

        if (
            sliding_window.count(self.opponent) == 3
            and sliding_window.count(Colour.GRAY) == 1
        ):
            score -= 4

        return score

    def __centre_score(self, board: Board, colour: Colour) -> int:
        score: int = 0
        # TODO: Implement this section

        centre: int = board.dimensions.x // 2

        sliding_window = [
            i
            for i in list(
                board[row][centre].get_token_colour()
                for row in range(board.dimensions.y)
            )
        ]

        score += sliding_window.count(colour) * 3

        return score

    def __horizontal_score(self, board: Board, colour: Colour) -> int:
        score: int = 0

        for row in range(board.dimensions.y):
            for col in range(board.dimensions.x - 3):
                sliding_window = [
                    board[row][col + i].get_token_colour() for i in range(WINDOW_SIZE)
                ]

                score += self.__evaluate_sliding_window(sliding_window, colour)

        return score

    def __vertical_score(self, board: Board, colour: Colour) -> int:
        score: int = 0

        for col in range(board.dimensions.x):
            for row in range(board.dimensions.y - 3):
                sliding_window = [
                    board[row + i][col].get_token_colour() for i in range(WINDOW_SIZE)
                ]

                score += self.__evaluate_sliding_window(sliding_window, colour)

        return score

    def __diagonal_score(self, board: Board, colour: Colour) -> int:
        score: int = 0

        for row in range(board.dimensions.y - 3):
            for col in range(board.dimensions.x - 3):
                sliding_window = [
                    board[row + i][col + i].get_token_colour()
                    for i in range(WINDOW_SIZE)
                ]

                score += self.__evaluate_sliding_window(sliding_window, colour)

        return score
