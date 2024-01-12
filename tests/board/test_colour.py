"""
File: test_colour.py
Project: Connect Four
File Created: Monday, 1st January 2024 5:18:37 PM
Author: feaad
Email: antwi-donkor_f@outlook.com
Version: 1.0
Brief: This file contains tests for the Colour class.
-----
Last Modified: Thursday, 11th January 2024 11:43:01 AM
Modified By: feaad
-----
Copyright ©2024 feaad
"""


from connect_four.board.colour import Colour


def test_colour_red() -> None:
    """
    The function `test_colour_red` tests if the string representation of the
    `Colour.RED` object is equal to "R".

    """
    result = str(Colour.RED)
    expected = "R"

    assert result == expected


def test_colour_yellow() -> None:
    """
    The function `test_colour_yellow` tests if the string representation of the
    `Colour.YELLOW` object is equal to "Y".

    """
    result = str(Colour.YELLOW)
    expected = "Y"

    assert result == expected


def test_colour_gray() -> None:
    """
    The function `test_colour_gray` tests if the string representation of the
    `Colour.GRAY` object is equal to the expected value "G".

    """
    result = str(Colour.GRAY)
    expected = "G"

    assert result == expected


def test_hashable() -> None:
    """
    The function `test_hashable` checks if a set of colours contains three
    distinct colours.

    """
    result = len(set([Colour.RED, Colour.YELLOW, Colour.GRAY]))
    expected = 3

    assert result == expected
