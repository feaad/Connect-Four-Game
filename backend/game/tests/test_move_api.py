import uuid
from typing import List

from core.constants import (
    CONNECT,
    DEFAULT_COLUMNS,
    DEFAULT_ROWS,
    EMPTY,
    PLAYER_ONE,
    PLAYER_TWO,
)
from core.models import Move, Player
from core.tests.helper import (
    create_game,
    create_guest,
    create_status,
    create_user,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from game.serializers import MoveSerializer

MOVE_URL = reverse("game:move-list")


def detail_url(move_id) -> str:
    """
    Return move detail URL.

    """

    return reverse("game:move-detail", args=[move_id])


def undo_url(move_id) -> str:
    """
    Return move undo URL.

    """

    return reverse("game:move-undo", args=[move_id])


def winning_board(token: int) -> List[List[int]]:
    """
    Return a winning board.

    """
    p1 = PLAYER_ONE if token == PLAYER_ONE else PLAYER_TWO
    p2 = PLAYER_TWO if token == PLAYER_ONE else PLAYER_ONE

    board = [
        [EMPTY for _ in range(DEFAULT_COLUMNS)] for _ in range(DEFAULT_ROWS)
    ]

    for i in range(CONNECT - 1):
        board[-1][i] = p1
        board[-2][i] = p2

    return board


class PrivateUserAPITests(APITestCase):
    """
    API Requests that do require Authentication

    """

    def setUp(self) -> None:
        self.user = create_user("username", email="username@example.com")
        self.guest = create_guest("utest_guest")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.created_status = create_status("Created")
        create_status("In Progress")
        create_status("Draw")
        self.p1w_status = create_status("Player 1 Wins")
        self.p2w_status = create_status("Player 2 Wins")
        self.game = create_game(self.user, self.guest, self.created_status)

    def test_create_move(self) -> None:
        """
        Test creating a new move.

        """

        row, column = 5, 1
        data = {
            "game_id": self.game.game_id,
            "row": row,
            "column": column,
        }

        response = self.client.post(MOVE_URL, data)

        self.game.refresh_from_db()

        move = Move.objects.all().first()
        serializer = MoveSerializer(move)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.game.board[row][column], PLAYER_ONE)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(self.game.status.name, "In Progress")

    def test_create_move_for_invalid_game(self) -> None:
        """
        Test creating a new move for an invalid game.

        """

        data = {
            "game_id": uuid.uuid4(),
        }

        response = self.client.post(MOVE_URL, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Game does not exist")

    def test_create_move_for_dif_game(self) -> None:
        """
        Test creating a new move for a different game.

        """
        row, column = 5, 1

        game = create_game(
            create_guest("test_guest1"),
            create_guest("test_guest2"),
            self.created_status,
        )

        data = {
            "game_id": game.game_id,
            "row": row,
            "column": column,
        }

        response = self.client.post(MOVE_URL, data)
        game.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "You are not a player in this game"
        )
        self.assertEqual(self.game.board[row][column], EMPTY)
        self.assertEqual(self.game.status.name, "Created")

    def test_create_move_for_not_in_progress_game(self) -> None:
        """
        Test creating a new move for a game that is not in progress.

        """

        game = create_game(self.user)

        data = {
            "game_id": game.game_id,
        }

        response = self.client.post(MOVE_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Game is not in progress")

    def test_create_move_when_not_turn(self) -> None:
        """
        Test creating a new move when it is not the player's turn.

        """

        game = create_game(
            create_guest("test_guest2"),
            self.user,
            self.created_status,
        )

        data = {
            "game_id": game.game_id,
        }

        response = self.client.post(MOVE_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "It is not your turn")

    def test_create_move_with_full_board(self) -> None:
        """
        Test creating a new move when the board is full.

        """

        game = create_game(self.user, status=self.created_status)
        game.board = [
            [
                PLAYER_ONE if (row + col) % 2 == 0 else PLAYER_TWO
                for col in range(DEFAULT_COLUMNS)
            ]
            for row in range(DEFAULT_ROWS)
        ]

        game.save()

        data = {
            "game_id": game.game_id,
        }

        response = self.client.post(MOVE_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Board is full")

    def test_create_move_with_no_row(self) -> None:
        """
        Test creating a new move with an invalid row.

        """

        data = {
            "game_id": self.game.game_id,
            "column": 5,
        }

        response = self.client.post(MOVE_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Column and Row are required")

    def test_create_move_with_no_column(self) -> None:
        """
        Test creating a new move with an no column.

        """

        data = {
            "game_id": self.game.game_id,
            "row": 5,
        }

        response = self.client.post(MOVE_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Column and Row are required")

    def test_create_move_with_no_column_and_row(self) -> None:
        """
        Test creating a new move with an no column.

        """

        data = {"game_id": self.game.game_id}

        response = self.client.post(MOVE_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Column and Row are required")

    def test_create_move_with_out_of_bounds_column(self) -> None:
        """
        Test creating a new move with an out of bounds column.

        """

        data = {
            "game_id": self.game.game_id,
            "row": 5,
            "column": DEFAULT_COLUMNS + 1,
        }

        response = self.client.post(MOVE_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"],
            "(Column,Row) must be less than "
            + f"({self.game.columns},{self.game.rows})",
        )

    def test_create_move_with_out_of_bounds_row(self) -> None:
        """
        Test creating a new move with an out of bounds row.

        """

        data = {
            "game_id": self.game.game_id,
            "row": DEFAULT_ROWS + 1,
            "column": 2,
        }

        response = self.client.post(MOVE_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"],
            "(Column,Row) must be less than "
            + f"({self.game.columns},{self.game.rows})",
        )

    def test_create_move_with_string_column(self) -> None:
        """
        Test creating a new move with a string column.

        """

        data = {
            "game_id": self.game.game_id,
            "row": 5,
            "column": "invalid",
        }

        response = self.client.post(MOVE_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Column and Row must be integers"
        )

    def test_create_move_with_string_row(self) -> None:
        """
        Test creating a new move with a string row.

        """

        data = {
            "game_id": self.game.game_id,
            "row": "invalid",
            "column": 5,
        }

        response = self.client.post(MOVE_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Column and Row must be integers"
        )

    def test_create_move_invalid_move(self) -> None:
        """
        Test creating a new move with an invalid move.

        """

        data = {
            "game_id": self.game.game_id,
            "row": DEFAULT_ROWS - 2,
            "column": DEFAULT_COLUMNS - 2,
        }

        response = self.client.post(MOVE_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid move")

    def test_create_p1_winning_move(self) -> None:
        """
        Test creating a winning move for player one.

        """
        token = PLAYER_ONE

        self.game.board = winning_board(token)

        self.game.save()

        data = {
            "game_id": self.game.game_id,
            "row": DEFAULT_ROWS - 1,
            "column": CONNECT - 1,
        }

        response = self.client.post(MOVE_URL, data)

        self.game.refresh_from_db()
        move = Move.objects.all().first()
        serializer = MoveSerializer(move)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(self.game.board[DEFAULT_ROWS - 1][CONNECT - 1], token)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(self.game.status.name, self.p1w_status.name)
        self.assertEqual(self.game.winner, self.game.player_one)
        self.assertEqual(self.game.current_turn, self.game.player_one)
        self.assertIsNotNone(self.game.end_time)

        self.assertGreater(self.game.player_one.elo, 1200)
        self.assertEqual(self.game.player_one.wins, 1)
        self.assertEqual(self.game.player_one.losses, 0)
        self.assertEqual(self.game.player_two.draws, 0)
        self.assertEqual(self.game.player_one.total_games, 1)

        self.assertLess(self.game.player_two.elo, 1200)
        self.assertEqual(self.game.player_two.wins, 0)
        self.assertEqual(self.game.player_two.losses, 1)
        self.assertEqual(self.game.player_two.draws, 0)
        self.assertEqual(self.game.player_two.total_games, 1)

    def test_create_p2_winning_move(self) -> None:
        """
        Test creating a winning move for player two.

        """
        token = PLAYER_TWO
        game = create_game(
            create_guest("test_guest1"), self.user, status=self.created_status
        )
        game.board = winning_board(token)
        game.current_turn = game.player_two

        game.save()

        data = {
            "game_id": game.game_id,
            "row": DEFAULT_ROWS - 1,
            "column": CONNECT - 1,
        }

        response = self.client.post(MOVE_URL, data)

        game.refresh_from_db()
        move = Move.objects.all().first()
        serializer = MoveSerializer(move)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(game.board[DEFAULT_ROWS - 1][CONNECT - 1], token)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(game.status.name, self.p2w_status.name)
        self.assertEqual(game.winner, game.player_two)
        self.assertEqual(game.current_turn, game.player_two)
        self.assertIsNotNone(game.end_time)

        self.assertLess(game.player_one.elo, 1200)
        self.assertEqual(game.player_one.wins, 0)
        self.assertEqual(game.player_one.losses, 1)
        self.assertEqual(game.player_two.draws, 0)
        self.assertEqual(game.player_one.total_games, 1)

        self.assertGreater(game.player_two.elo, 1200)
        self.assertEqual(game.player_two.wins, 1)
        self.assertEqual(game.player_two.losses, 0)
        self.assertEqual(game.player_two.draws, 0)
        self.assertEqual(game.player_two.total_games, 1)

    def test_create_draw_move(self) -> None:
        """
        Test creating a draw move.

        """
        l1 = [PLAYER_TWO, PLAYER_ONE] * 3 + [PLAYER_TWO]
        l2 = [PLAYER_ONE, PLAYER_TWO] * 3 + [PLAYER_ONE]

        row = 0
        column = DEFAULT_COLUMNS - 1

        game = create_game(self.user, status=self.created_status)

        game.board = [
            [PLAYER_ONE, PLAYER_TWO] * 3 + [EMPTY],
            l2,
            l1,
            l2,
            l2,
            l1,
        ]

        game.save()

        data = {
            "game_id": game.game_id,
            "row": row,
            "column": column,
        }

        response = self.client.post(MOVE_URL, data)

        game.refresh_from_db()
        move = Move.objects.all().first()
        serializer = MoveSerializer(move)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(game.board[row][column], PLAYER_ONE)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(game.status.name, "Draw")
        self.assertIsNone(game.winner)
        self.assertEqual(game.current_turn, game.player_one)
        self.assertIsNotNone(game.end_time)

        self.assertEqual(game.player_one.elo, 1200)
        self.assertEqual(game.player_one.wins, 0)
        self.assertEqual(game.player_one.losses, 0)
        self.assertEqual(game.player_two.draws, 1)
        self.assertEqual(game.player_one.total_games, 1)

        self.assertEqual(game.player_two.elo, 1200)
        self.assertEqual(game.player_two.wins, 0)
        self.assertEqual(game.player_two.losses, 0)
        self.assertEqual(game.player_two.draws, 1)
        self.assertEqual(game.player_two.total_games, 1)

    def test_undo_move(self) -> None:
        """
        Test undoing a move.

        """

        row, column = 5, 1
        player = Player.objects.get(user=self.user)

        move = Move.objects.create(
            game=self.game,
            player=player,
            row=row,
            column=column,
        )

        self.game.refresh_from_db()
        response = self.client.post(undo_url(self.game.game_id))

        self.game.refresh_from_db()
        move.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.game.board[row][column], EMPTY)
        self.assertEqual(self.game.status.name, "In Progress")
        self.assertEqual(self.game.current_turn, player)
        self.assertTrue(move.is_undone)

    def test_undo_move_invalid_game_id(self) -> None:
        """
        Test undoing a move with an invalid game id.

        """

        response = self.client.post(undo_url(uuid.uuid4()))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "No moves to undo")

    def test_cannot_undo_move(self) -> None:
        """
        Test undoing a move when there are no moves to undo.

        """
        player = Player.objects.get(user=self.user)
        Move.objects.create(
            game=self.game,
            player=player,
            row=5,
            column=1,
        )
        self.game.refresh_from_db()
        Move.objects.create(
            game=self.game,
            player=Player.objects.get(guest=self.guest),
            row=4,
            column=1,
        )
        self.game.refresh_from_db()

        response = self.client.post(undo_url(self.game.game_id))
        self.game.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "You cannot undo this move")
        self.assertEqual(self.game.current_turn, player)

    def test_retrieve_move_list(self) -> None:
        """
        Test retrieving a list of moves.

        """
        Move.objects.create(
            game=self.game,
            player=Player.objects.get(user=self.user),
            row=5,
            column=1,
        )
        Move.objects.create(
            game=self.game,
            player=Player.objects.get(guest=self.guest),
            row=4,
            column=1,
        )

        response = self.client.get(MOVE_URL)

        moves = Move.objects.all().order_by("updated_at")
        serializer = MoveSerializer(moves, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_move(self) -> None:
        """
        Test retrieving a move.

        """
        move = Move.objects.create(
            game=self.game,
            player=Player.objects.get(user=self.user),
            row=5,
            column=1,
        )

        response = self.client.get(detail_url(move.move_id))

        serializer = MoveSerializer(move)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_moves_by_search(self) -> None:
        """
        Test retrieving moves by search.

        """

        Move.objects.create(
            game=self.game,
            player=Player.objects.get(user=self.user),
            row=5,
            column=1,
        )
        Move.objects.create(
            game=self.game,
            player=Player.objects.get(guest=self.guest),
            row=4,
            column=1,
        )

        response = self.client.get(
            MOVE_URL, {"search": str(self.game.game_id)}
        )

        moves = Move.objects.all().order_by("updated_at")
        serializer = MoveSerializer(moves, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)
