"""
File: position.py
Project: Connect Four
File Created: Monday, 1st January 2024 4:29:08 PM
Author: feaad
Email: antwi-donkor_f@outlook.com
Version: 1.0
Brief: Defines a position on the board
-----
Last Modified: Monday, 1st January 2024 4:33:58 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from dataclasses import dataclass


@dataclass
class Position:
    """Defines a position on the board"""

    x: int  # The x coordinate of the position or column
    y: int  # The y coordinate of the position or row

    def __str__(self) -> str:
        """
        The function returns a string representation of the Position object
        with its x and y coordinates.

        Returns
        -------
            The `__str__` method is returning a string representation of the
            object's coordinates in the format "(x, y)".

        """
        return f"({self.x}, {self.y})"
