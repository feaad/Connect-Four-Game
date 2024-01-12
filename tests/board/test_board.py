"""
File: test_board.py
Project: Connect Four
File Created: Monday, 1st January 2024 5:19:18 PM
Author: feaad
Email: antwi-donkor_f@outlook.com
Version: 1.0
Brief: This file contains tests for the Board class.
-----
Last Modified: Thursday, 11th January 2024 11:32:15 AM
Modified By: feaad
-----
Copyright ©2024 feaad
"""
from unittest.mock import MagicMock, call, patch

from connect_four.board.board import Board
from connect_four.board.colour import Colour
from connect_four.board.position import Position

WIDTH = 9
HEIGHT = 11


class TestBoard:
    """This class contains tests for the Board class."""

    def setup_method(self) -> None:
        """
        The `setup_method` method initializes the `board` attribute of the
        object.

        """
        dimensions = Position(WIDTH, HEIGHT)
        self.board = Board(dim=dimensions)

    def teardown_method(self) -> None:
        """
        The `teardown_method` function deletes the `board` attribute of the
        object.

        """
        del self.board

    @patch("builtins.print")
    def test_print_board(self, mock_print: MagicMock) -> None:
        """
        The function `test_print_board` tests the `print_board` method of a
        `board` object by mocking the `print` function and asserting that it is
        called with the correct arguments.

        Parameters
        ----------
        mock_print : MagicMock
            The parameter `mock_print` is a MagicMock object. It is used to
            mock the `print` function so that we can assert the calls made to
            it. By using a MagicMock object, we can check if the `print`
            function was called with the expected arguments.

        """
        row = (WIDTH - 1) * "G " + "G"

        self.board.print_board()
        calls = [call(row) for _ in range(HEIGHT)]

        mock_print.assert_has_calls(calls, any_order=True)

    def test_is_full(self) -> None:
        """
        The function `test_is_full` checks if the game board is full after
        dropping tokens in all columns.

        """
        assert not self.board.is_full()

        for _ in range(HEIGHT):
            for x in range(1, WIDTH + 1):
                self.board.drop_token(column=x, colour=Colour.RED)

        assert self.board.is_full()

    def test_drop_token(self) -> None:
        """
        The function tests the drop_token method of the board object by
        dropping a red token in column 1.

        """
        assert self.board.drop_token(column=1, colour=Colour.RED)

    def test_drop_token_out_of_bounds(self) -> None:
        """
        The function tests if dropping a token outside the bounds of the board
        returns False.

        """
        assert not self.board.drop_token(column=0, colour=Colour.RED)

        assert not self.board.drop_token(column=WIDTH + 1, colour=Colour.RED)

    def test_drop_token_full_column(self) -> None:
        """
        The function tests if a token can be dropped in a full column of a
        board.

        """
        for _ in range(HEIGHT):
            self.board.drop_token(column=1, colour=Colour.RED)

        assert not self.board.drop_token(column=1, colour=Colour.RED)

    def test_vertical_win(self) -> None:
        """
        The function tests for a vertical win condition in a game board.

        """
        for _ in range(HEIGHT):
            self.board.drop_token(column=1, colour=Colour.RED)

        assert self.board.check_win()

    def test_vertical_no_win(self) -> None:
        """
        The function tests if there is no vertical win condition in a Connect
        Four game.

        """
        for i in range(HEIGHT):
            if (i + 1) % 2 == 0:
                self.board.drop_token(column=1, colour=Colour.RED)
            else:
                self.board.drop_token(column=1, colour=Colour.YELLOW)

        assert not self.board.check_win()

    def test_horizontal_win_on_right(self) -> None:
        """
        The function tests for a horizontal win on the right side of the game
        board.

        """
        for x in range(WIDTH):
            self.board.drop_token(column=x, colour=Colour.RED)

        assert self.board.check_win()

    def test_horizontal_win_on_left(self) -> None:
        """
        The function tests for a horizontal win on the left side of the game
        board.

        """
        for x in range(WIDTH - 1, -1, -1):
            self.board.drop_token(column=x, colour=Colour.RED)

        assert self.board.check_win()

    def test_horizontal_win_on_middle(self) -> None:
        """
        The function tests for a horizontal win on the middle row of a game
        board.

        """
        # Fill the left half of the board with Colour.RED tokens.
        for x in range(WIDTH // 2):
            self.board.drop_token(column=x, colour=Colour.RED)

        # Fill the right half of the board with Colour.YELLOW tokens.
        for x in range(WIDTH // 2 + 1, WIDTH - 1):
            self.board.drop_token(column=x, colour=Colour.YELLOW)

        self.board.drop_token(column=WIDTH // 2, colour=Colour.RED)

        assert self.board.check_win()

    def test_horizontal_no_win(self) -> None:
        """
        The function tests for a horizontal win condition on a game board.

        """
        for x in range(WIDTH):
            if (x + 1) % 2 == 0:
                self.board.drop_token(column=x, colour=Colour.RED)
            else:
                self.board.drop_token(column=x, colour=Colour.YELLOW)

        assert not self.board.check_win()

    def test_diagonal_win_right_up(self) -> None:
        """
        The function tests for a diagonal win in the upward right direction on
        a game board.

        """
        self.board.drop_token(column=1, colour=Colour.RED)
        self.board.drop_token(column=2, colour=Colour.YELLOW)
        self.board.drop_token(column=2, colour=Colour.RED)
        self.board.drop_token(column=3, colour=Colour.YELLOW)
        self.board.drop_token(column=3, colour=Colour.YELLOW)
        self.board.drop_token(column=3, colour=Colour.RED)
        self.board.drop_token(column=4, colour=Colour.YELLOW)
        self.board.drop_token(column=4, colour=Colour.YELLOW)
        self.board.drop_token(column=4, colour=Colour.YELLOW)

        self.board.drop_token(column=4, colour=Colour.RED)

        assert self.board.check_win()

    def test_diagonal_win_left_down(self) -> None:
        """
        The function tests for a diagonal win from the bottom left to the top
        right on a game board.

        """
        self.board.drop_token(column=1, colour=Colour.RED)
        self.board.drop_token(column=1, colour=Colour.YELLOW)
        self.board.drop_token(column=1, colour=Colour.YELLOW)
        self.board.drop_token(column=1, colour=Colour.YELLOW)
        self.board.drop_token(column=2, colour=Colour.RED)
        self.board.drop_token(column=2, colour=Colour.YELLOW)
        self.board.drop_token(column=2, colour=Colour.YELLOW)
        self.board.drop_token(column=3, colour=Colour.RED)
        self.board.drop_token(column=3, colour=Colour.YELLOW)

        self.board.drop_token(column=4, colour=Colour.RED)

        assert self.board.check_win()

    def test_diagonal_win_middle(self) -> None:
        """
        The function tests for a diagonal win in the middle of the game board.

        """
        self.board.drop_token(column=1, colour=Colour.RED)
        self.board.drop_token(column=1, colour=Colour.YELLOW)
        self.board.drop_token(column=1, colour=Colour.YELLOW)
        self.board.drop_token(column=1, colour=Colour.YELLOW)
        self.board.drop_token(column=2, colour=Colour.RED)
        self.board.drop_token(column=2, colour=Colour.YELLOW)
        self.board.drop_token(column=3, colour=Colour.RED)
        self.board.drop_token(column=3, colour=Colour.YELLOW)
        self.board.drop_token(column=4, colour=Colour.YELLOW)

        self.board.drop_token(column=2, colour=Colour.YELLOW)

        assert self.board.check_win()

    def test_diagonal_no_win(self) -> None:
        """
        The function tests for a diagonal win condition in a Connect Four game.

        """
        self.board.drop_token(column=1, colour=Colour.RED)
        self.board.drop_token(column=1, colour=Colour.YELLOW)
        self.board.drop_token(column=1, colour=Colour.YELLOW)
        self.board.drop_token(column=1, colour=Colour.YELLOW)
        self.board.drop_token(column=2, colour=Colour.RED)
        self.board.drop_token(column=2, colour=Colour.YELLOW)
        self.board.drop_token(column=3, colour=Colour.RED)
        self.board.drop_token(column=3, colour=Colour.YELLOW)
        self.board.drop_token(column=4, colour=Colour.YELLOW)

        self.board.drop_token(column=2, colour=Colour.RED)

        assert not self.board.check_win()
