"""
File: player.py
Project: Connect Four
File Created: Monday, 12th February 2024 10:26:43 AM
Author: feaad
Email: antwi-donkor_f@outlook.com
Version: 1.0
Brief: Implementation of the Player Base class
-----
Last Modified: Monday, 12th February 2024 10:37:15 AM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from typing import Optional

from board.board import Board
from board.colour import Colour


class Player:
    """Implementation of the Player Base class"""

    name: str
    colour: Colour
    is_turn: bool

    def __init__(self, name: str, colour: Colour) -> None:
        """
        The function initializes an object with a name and a colour, and sets
        the is_turn attribute to False.

        Parameters
        ----------
        name : str
            The name parameter is a string that represents the name of an
            object.

        colour : Colour
            The "colour" parameter is of type "Colour". It is used to specify
            the color of an object.

        """
        self.name = name
        self.colour = colour
        self.is_turn = False

    def get_name(self) -> str:
        """
        The function `get_name` returns the name attribute of an object.

        Returns
        -------
            The name of the object.

        """
        return self.name

    def set_is_turn(self, is_turn: bool) -> None:
        """
        The function sets the value of the "is_turn" attribute to True.

        Parameters
        ----------
        is_turn : bool
            The parameter `is_turn` is a boolean value that indicates whether it is currently the turn of
        the object or not.

        """
        self.is_turn = is_turn

    def get_colour(self) -> Colour:
        """
        The function `get_colour` returns the colour of an object.

        Returns
        -------
            The method is returning the value of the "colour" attribute.

        """
        return self.colour

    def get_move(self, board: Optional[Board] = None) -> int:
        """
        The `get_move` function is a method that must be implemented by a
        subclass of Player and it returns an integer.

        Parameters
        ----------
        board : Optional[Board]
            The `board` parameter is an optional argument of type `Board`. It
            represents the current state of the game board.

        """
        raise NotImplementedError(
            "This method must be implemented by a subclass of Player"
        )
