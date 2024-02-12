"""
File: human.py
Project: Connect Four
File Created: Monday, 12th February 2024 10:26:56 AM
Author: feaad
Email: antwi-donkor_f@outlook.com
Version: 1.0
Brief: Implementation of the Human Player
-----
Last Modified: Monday, 12th February 2024 10:46:14 AM
Modified By: feaad
-----
Copyright ©2024 feaad
"""


from typing import Optional

from board.board import Board
from board.colour import Colour

from .player import Player


class Human(Player):
    """Implementation of the Human Player"""

    def __init__(self, name: str, colour: Colour) -> None:
        """
        The above function is a constructor that initializes an object with a name and a colour.

        Parameters
        ----------
        name : str
            The name parameter is a string that represents the name of an object.
        colour : Colour
            The "colour" parameter is of type "Colour". It is used to specify the color of an object.

        """
        super().__init__(name, colour)

    def get_move(self, board: Optional[Board] = None) -> int:
        """
        The function prompts the user to enter a column number and returns the
        input as an integer.

        Parameters
        ----------
        board : Optional[Board]
            The `board` parameter is an optional argument of type `Board`. It
            represents the current state of the game board.

        Returns
        -------
            the column number entered by the user, after subtracting 1 from it.

        """
        if not self.is_turn:
            raise ValueError(f"It's not the {self.name}'s turn")

        # TODO: Clean the .value.symbol
        column = (
            int(
                input(
                    f"{self.colour.value.symbol} {self.name}, kindly enter the column number: "
                )
            )
            - 1
        )

        return column
