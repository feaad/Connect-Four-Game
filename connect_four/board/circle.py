"""
File: circle.py
Project: Connect Four
File Created: Monday, 1st January 2024 5:01:21 PM
Author: feaad
Email: antwi-donkor_f@outlook.com
Version: 1.0
Brief: A Circle represents a circle on the board.
-----
Last Modified: Tuesday, 2nd January 2024 10:50:33 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from .colour import Colour
from .position import Position
from .token import Token


class Circle:
    """A Representation of a Circle on the Board"""

    token: Token  # The token on the circle
    position: Position  # The position of the circle

    def __init__(self, *, position: Position) -> None:
        """
        The function initializes an object with a given position and sets its
        token colour to gray.

        Parameters
        ----------
        position : Position
            The `position` parameter is of type `Position`. It represents the
            position of an object in a coordinate system.

        """
        self.position = position
        self.token = Token(colour=Colour.GRAY)

    def is_occupied(self) -> bool:
        """
        The function checks if a chessboard square is occupied by a token or
        not.

        Returns
        -------
            a boolean value. If the `token` attribute of the object is not
            `None`, then `True` is returned. Otherwise, `False` is returned.

        """
        if self.token.get_colour() != Colour.GRAY:
            return True

        return False

    def get_token(self) -> Token:
        """
        The function returns the token associated with an object.

        Returns
        -------
            The method is returning the value of the variable "token".

        """
        return self.token

    def set_token(self, *, colour: Colour) -> None:
        """
        The function sets the token colour for a given object.

        Parameters
        ----------
        colour : Colour
            The `colour` parameter is a variable that represents the colour of
            a game token. It is of type `Colour`, which is a custom class and
            an enumeration that defines different colours.

        """
        self.token = Token(colour=colour)

    def __str__(self) -> str:
        """
        The function returns a string representation of the object.

        Returns
        -------
            A string representation of the object.

        """
        return str(self.token)

    def __eq__(self, other: object) -> bool:
        """
        The function checks if two objects are equal.

        Parameters
        ----------
        other : object
            The `other` parameter is an object that is being compared with the
            current object.

        Returns
        -------
            A boolean value. If the two objects are equal, then `True` is
            returned. Otherwise, `False` is returned.

        """
        if not isinstance(other, Circle):
            return NotImplemented

        return self.token == other.token
