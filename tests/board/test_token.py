"""
File: test_token.py
Project: Connect Four
File Created: Monday, 1st January 2024 5:18:48 PM
Author: feaad
Email: antwi-donkor_f@outlook.com
Version: 1.0
Brief: This file contains tests for the Token data class.
-----
Last Modified: Thursday, 11th January 2024 11:45:10 AM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from connect_four.board.colour import Colour
from connect_four.board.token import Token


class TestToken:
    """This class contains tests for the Token data class."""

    def setup_method(self) -> None:
        """
        The `setup_method` method initializes a token object with the colour
        attribute set to red.

        """
        self.token = Token(colour=Colour.RED)

    def teardown_method(self) -> None:
        """
        The `teardown_method` function deletes the `token` attribute from the
        object.

        """
        del self.token

    def test_get_colour(self) -> None:
        """
        The function `test_get_colour` tests the `get_colour` method of a
        `token` object and asserts that it returns the `Colour.RED` value.

        """
        assert self.token.get_colour() == Colour.RED

    def test_equal(self) -> None:
        """
        The function tests if the token's colour is red.

        """
        assert self.token == Token(colour=Colour.RED)

    def test_not_equal(self) -> None:
        """
        The function tests if a token is not equal to a token with a specific
        colour.

        """
        assert self.token != Token(colour=Colour.GRAY)

    def test_str(self) -> None:
        """
        The function tests if the string representation of a token object is
        equal to "R".

        """
        assert str(self.token) == "R"
