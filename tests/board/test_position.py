"""
File: test_position.py
Project: Connect Four
File Created: Monday, 1st January 2024 5:19:02 PM
Author: feaad
Email: antwi-donkor_f@outlook.com
Version: 1.0
Brief: This file contains tests for the Position data class.
-----
Last Modified: Thursday, 11th January 2024 11:44:33 AM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from connect_four.board.position import Position


def test_position() -> None:
    """
    The function `test_position` tests the `Position` data class by creating an
    instance of it and asserting that its `x` and `y` attributes are equal to
    the provided values.

    """
    x, y = 1, 2

    position = Position(x, y)

    assert position.x == x
    assert position.y == y


def test_position_str() -> None:
    """
    The function `test_position_str` tests the `str` method of the `Position`
    class to ensure it returns the expected string representation of the
    position.

    """
    x, y = 1, 2

    position = Position(x, y)

    expected = str(position)
    result = f"({x}, {y})"

    assert result == expected
