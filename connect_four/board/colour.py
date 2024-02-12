"""
File: colour.py
Project: Connect Four
File Created: Monday, 1st January 2024 4:37:47 PM
Author: feaad
Email: antwi-donkor_f@outlook.com
Version: 1.0
Brief: Defines the colours of the game tokens
-----
Last Modified: Monday, 1st January 2024 4:42:39 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""


from dataclasses import dataclass
from enum import Enum


@dataclass
class ColourSymbol:
    """Defines the attributes of the ColourSymbol class"""

    name: str
    value: int
    symbol: str
    win_symbol: str

    @property
    def raw(self):
        """
        The function returns the symbol attribute of the object.

        Returns
        -------
            The symbol attribute of the object.

        """
        return self.value


class Colour(Enum):
    """Defines the colours of the game tokens"""

    GRAY = ColourSymbol("GRAY", 0, "  ", "  ")
    RED = ColourSymbol("RED", 1, "🔴", "🟥")
    YELLOW = ColourSymbol("YELLOW", 2, "🟡", "🟨")

    def __str__(self):
        """
        The function returns the first character of the value attribute,
        capitalized.

        Returns
        -------
            The first character of the value attribute, converted to uppercase.

        """
        return self.value.name.upper()

    def __eq__(self, other: object):
        """
        The function checks if two objects of the Colour class are equal by
        comparing their values.

        Parameters
        ----------
        other : object
            The "other" parameter is an object that we are comparing to the
            current object for equality.

        Returns
        -------
            The `__eq__` method is returning `True` if the `other` object is an
            instance of the `Colour` class and has the same `value` attribute
            as the current object (`self`). Otherwise, it returns `False`.

        """
        if isinstance(other, Colour):
            return self.value == other.value

        return False

    def __hash__(self):
        """
        The function returns the hash value of the "value" attribute of the
        object.

        Returns
        -------
            The hash value of the "value" attribute of the object.

        """
        return hash(self.value)
