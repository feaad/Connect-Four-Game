"""
File: token.py
Project: Connect Four
File Created: Monday, 1st January 2024 4:45:02 PM
Author: feaad
Email: antwi-donkor_f@outlook.com
Version: 1.0
Brief: The class represents a token on the board.
-----
Last Modified: Monday, 1st January 2024 4:59:59 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from .colour import Colour


class Token:
    """The class represents a token on the board."""

    colour: Colour

    def __init__(self, *, colour: Colour) -> None:
        """
        The function initializes an object with a specified colour.

        Parameters
        ----------
        colour : Colour
            The "colour" parameter is a variable that represents the colour of
            an object. It is of type "Colour", which is a custom class or
            enumeration that defines different colours.

        """
        self.colour = colour

    def get_colour(self) -> Colour:
        """
        The function returns the colour of an object.

        Returns
        -------
            The method is returning the value of the "colour" attribute.

        """

        return self.colour

    def __eq__(self, other: object) -> bool:
        """
        The function checks if two objects are equal by comparing their
        colours.

        Parameters
        ----------
        other : object
            The "other" parameter is an object that we are comparing to the
            current object.

        Returns
        -------
            The code is returning a boolean value. If the "other" object is an
            instance of the "Token" class and the "colour" attribute of both
            objects is the same, then it returns True. Otherwise, it returns
            False.

        """
        if isinstance(other, Token):
            return self.colour == other.colour

        return False

    def __str__(self) -> str:
        """
        The __str__ function returns a string representation of the colour
        attribute.

        Returns
        -------
            The `__str__` method is returning the string representation of the
            `colour` attribute.

        """
        return str(self.colour)
