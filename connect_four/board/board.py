"""
File: board.py
Project: Connect Four
File Created: Monday, 1st January 2024 5:16:24 PM
Author: feaad
Email: antwi-donkor_f@outlook.com
Version: 1.0
Brief: A Board represents a Connect Four board.
-----
Last Modified: Tuesday, 2nd January 2024 10:50:15 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from typing import List, Set

from .circle import Circle
from .colour import Colour
from .position import Position


class Board:
    """A Board represents a Connect Four board."""

    # The representation below shows the indices of the board.
    # The board is represented as a 2D array of Circles.

    #                   Columns(Width)
    #                  0 1 2 3 4 5 6 7
    #               0 | | | | | | | | |
    #               1 | | | | | | | | |
    #               2 | | | | | | | | |
    # Rows(height)  3 | | | | | |P| | |
    #               4 | | | | | | | | |
    #               5 | | | | | | | | |
    #               6 |E| | | | | | |T|

    # (Width -> Column -> X = 8)
    # (Height -> Row -> Y = 7)

    # [Y][X]
    # T = [6][7]
    # P = [3][6]
    # E = [6][0]

    dimensions: Position  # The dimensions of the board

    max_tokens: int  # The maximum number of tokens allowed on the board
    num_tokens: int  # The number of tokens current on the board

    last_filled: Position  # The position of the last filled token

    board: List[List[Circle]]  # The board

    win_positions: Set[Position]  # The positions that make up a win

    def __init__(self, dim: Position) -> None:
        """
        The above function initializes a board with a given dimension and sets
        up the necessary variables for tracking the number of tokens on the
        board.

        Parameters
        ----------
        dim : Position
            The `dim` parameter is an instance of the `Position` class. It
            represents the dimensions of the board. The `dim` object has two
            attributes: `x` and `y`, which represent the number of columns and
            rows on the board, respectively.

        """
        self.dimensions = dim

        # Instantiation the board with dim.x columns and dim.y rows.
        self.board = [
            [Circle(position=Position(x, y)) for x in range(dim.x)]
            for y in range(dim.y)
        ]

        self.max_tokens = dim.x * dim.y
        self.num_tokens = 0

        self.last_filled = Position(-1, -1)

        self.win_positions = set()

    def print_board(self) -> None:
        """
        The `print_board` function prints the contents of a board in a grid
        format.

        """

        header = "\n\t" + "+----" * self.dimensions.x + "+"
        for row in range(self.dimensions.y):
            print(header)
            print("\t|", end="")
            for col in range(self.dimensions.x):
                if Position(col, row) in self.win_positions:
                    print(f" {self.board[row][col].get_token_win_symbol()}", end=" |")
                else:
                    print(f" {self.board[row][col].get_token_symbol()}", end=" |")
        print(header)
        print("\t " + " ".join(f" C{i+1} " for i in range(self.dimensions.x)))

    def is_full(self) -> bool:
        """
        The function checks if the number of tokens is equal to the maximum
        number of tokens.

        Returns
        -------
            The method is returning a boolean value indicating whether the
            number of tokens in the object is equal to the maximum number of
            tokens allowed.

        """
        return self.num_tokens == self.max_tokens

    def drop_token(self, column: int, colour: Colour) -> bool:
        """
        The `drop_token` function checks if a column is within the valid range,
        and if so, drops a token of a specified colour into the lowest
        available position in that column.

        Parameters
        ----------
        column : int
            The `column` parameter represents the column number where the token
            should be dropped. It is an integer value that indicates the column
            index, starting from 1.
        colour : Colour
            The "colour" parameter represents the colour of the token that is
            being dropped into the column. It is of type "Colour".

        Returns
        -------
            a boolean value. It returns True if the token was successfully
            dropped in the specified column, and False if the entire column is
            already occupied.

        """

        # Check if the column is within the valid range
        if not (0 <= column < self.dimensions.x):
            return False

        # Iterate from the bottom of the column upwards
        for y in range(self.dimensions.y - 1, -1, -1):
            # If the current position is not occupied, drop the token there
            if not self.board[y][column].is_occupied():
                self.board[y][column].set_token(colour=colour)
                self.last_filled = Position(column, y)
                self.num_tokens += 1
                return True

        # If the entire column is occupied, return False
        return False

    def get_open_columns(self) -> List[int]:
        """
        The function returns a list of column indices that are not full.

        Returns
        -------
            a list of column indices that are not full.

        """
        return [
            x for x in range(self.dimensions.x) if not self.board[0][x].is_occupied()
        ]

    def is_game_over(self) -> bool:
        """
        The function checks if the game is over by checking if there is a win
        condition or if the board is full.

        Returns
        -------
            a boolean value. It returns True if the game is over, and False
            otherwise.

        """
        return self.check_win() or self.is_full()

    def is_winner(self, colour: Colour) -> bool:
        """
        The function checks if a player with a specified colour has won the game.

        Parameters
        ----------
        colour : Colour
            The "colour" parameter represents the colour of the player. It is of
            type "Colour".

        Returns
        -------
            a boolean value. It returns True if the player with the specified
            colour has won the game, and False otherwise.

        """
        return (
            self.check_win()
            and self.board[self.last_filled.y][self.last_filled.x]
            .get_token()
            .get_colour()
            == colour
        )

    def check_win(self) -> bool:
        """
        The function checks if there is a win condition in a game by checking
        for horizontal, vertical, and diagonal matches.

        Returns
        -------
            a boolean value. It returns True if there is a win condition in
            the game, and False otherwise.

        """
        if self.num_tokens < 7:
            return False

        return (
            self.__check_horizontal_win()
            or self.__check_vertical_win()
            or self.__check_diagonal_win()
        )

    def __check_horizontal_win(self) -> bool:
        """
        The function checks if there is a horizontal win in a Connect Four game
        by counting the number of consecutive circles of the same colour in
        both directions from the last filled position.

        Returns
        -------
            a boolean value. It returns True if there is a horizontal win (four
            circles of the same colour in a row), and False otherwise.

        """
        last_circle = self.board[self.last_filled.y][self.last_filled.x]
        same_colour_count = 1
        win_positions: Set[Position] = {
            Position(self.last_filled.x, self.last_filled.y)
        }

        for dx in [-1, 1]:
            for d in range(1, 4):
                x = self.last_filled.x + dx * d

                if (
                    0 <= x < self.dimensions.x
                    and self.board[self.last_filled.y][x] == last_circle
                ):
                    same_colour_count += 1
                    win_positions.add(Position(x, self.last_filled.y))
                else:
                    break

                if same_colour_count >= 4:
                    self.win_positions.update(win_positions)
                    return True

        return False

    def __check_vertical_win(self) -> bool:
        """
        The function checks if there is a vertical win in a Connect Four game
        by counting the number of consecutive circles of the same colour below
        the last filled position.

        Returns
        -------
            a boolean value. It returns True if there is a vertical win (four
            circles of the same colour in a column), and False otherwise.

        """
        last_circle = self.board[self.last_filled.y][self.last_filled.x]
        same_colour_count = 1
        win_positions: Set[Position] = {
            Position(self.last_filled.x, self.last_filled.y)
        }

        for y in range(self.last_filled.y + 1, self.last_filled.y + 4):
            if (
                0 <= y < self.dimensions.y
                and self.board[y][self.last_filled.x] == last_circle
            ):
                same_colour_count += 1
                win_positions.add(Position(self.last_filled.x, y))
            else:
                break

            if same_colour_count >= 4:
                self.win_positions.update(win_positions)
                return True

        return False

    def __check_diagonal_win(self) -> bool:
        """
        The function checks if there is a diagonal win in a game board by
        counting the number of consecutive circles of the same colour in
        diagonal directions.

        Returns
        -------
            a boolean value. It returns True if there is a diagonal win (four
            circles of the same colour in a diagonal line), and False
            otherwise.

        """
        last_circle = self.board[self.last_filled.y][self.last_filled.x]
        win_positions: Set[Position] = {
            Position(self.last_filled.x, self.last_filled.y)
        }

        # The directions in which to check for a diagonal win
        directions = [(1, 1), (1, -1)]

        for dx, dy in directions:
            same_colour_count = 1

            for direction in [-1, 1]:
                for d in range(1, 4):
                    x, y = (
                        self.last_filled.x + direction * d * dx,
                        self.last_filled.y + direction * d * dy,
                    )

                    if (
                        (0 <= x < self.dimensions.x)
                        and (0 <= y < self.dimensions.y)
                        and self.board[y][x] == last_circle
                    ):
                        same_colour_count += 1
                        win_positions.add(Position(x, y))
                    else:
                        break

                    if same_colour_count >= 4:
                        self.win_positions.update(win_positions)
                        return True

        return False

    @property
    def raw(self) -> List[List[Circle]]:
        """
        The function returns the raw board.

        Returns
        -------
            the raw board.

        """
        return self.board

    def __getitem__(self, key: int) -> List[Circle]:
        """
        The function returns a row of the board.

        Parameters
        ----------
        key : int
            The `key` parameter is an integer that represents the row index.

        Returns
        -------
            a row of the board.

        """
        return self.board[key]