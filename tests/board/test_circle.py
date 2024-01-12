"""
File: test_circle.py
Project: Connect Four
File Created: Monday, 1st January 2024 5:18:27 PM
Author: feaad
Email: antwi-donkor_f@outlook.com
Version: 1.0
Brief: This file contains tests for the Circle class.
-----
Last Modified: Thursday, 11th January 2024 11:40:08 AM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from connect_four.board.circle import Circle
from connect_four.board.colour import Colour
from connect_four.board.position import Position
from connect_four.board.token import Token


class TestCircle:
    """This class contains tests for the Circle class."""

    def setup_method(self) -> None:
        """
        The `setup_method` method initializes a circle object with a position
        at (0, 0).

        """
        position = Position(0, 0)
        self.circle = Circle(position=position)

    def teardown_method(self) -> None:
        """
        The `teardown_method` function deletes the `circle` attribute from the
        object.

        """
        del self.circle

    def test_get_token(self) -> None:
        """
        The function `test_get_token` tests the `get_token` method of the
        `circle` object and asserts that it returns a gray token.

        """
        assert self.circle.get_token() == Token(colour=Colour.GRAY)

    def test_set_token(self) -> None:
        """
        The function `test_set_token` sets the token colour of a circle object
        to red.

        """
        self.circle.set_token(colour=Colour.RED)

        assert self.circle.get_token() == Token(colour=Colour.RED)

    def test_is_occupied(self) -> None:
        """
        The function `test_is_occupied` tests whether a circle is occupied or
        not.

        """
        assert not self.circle.is_occupied()

        self.circle.set_token(colour=Colour.RED)

        assert self.circle.is_occupied()

    def test_str(self) -> None:
        """
        The function tests the string representation of a circle object.

        """
        assert str(self.circle) == "G"

        self.circle.set_token(colour=Colour.RED)

        assert str(self.circle) == "R"
