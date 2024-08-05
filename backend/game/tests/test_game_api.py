from core.models import Game, Player, User
from core.tests.helper import (
    create_algorithm,
    create_guest,
    create_status,
    create_user,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from game.serializers import GameSerializer


def create_game(user: User) -> Game:
    """
    Helper function to create a game.

    """
    player_two = create_guest()
    status = create_status()

    return Game.objects.create(
        player_one=Player.objects.get(user=user),
        player_two=Player.objects.get(guest=player_two),
        status=status,
        current_turn=Player.objects.get(user=user),
        created_by=Player.objects.get(user=user),
    )


class PrivateUserAPITests(APITestCase):
    """
    API Requests that do require Authentication

    """

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        create_status("Created")
        create_algorithm("Minimax")

    def test_create_game(self):
        """
        Test creating a new game.

        """

        payload = {"algorithm": "Minimax", "play_preference": "first"}

        response = self.client.post(reverse("game:game:game-create"), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Game.objects.count(), 1)

    def test_retrieve_games(self):
        """
        Test retrieving a list of games.

        """

        create_game(self.user)
        create_game(self.user)

        response = self.client.get(reverse("game:game-list"))

        games = Game.objects.all().order_by("game_id")
        serializer = GameSerializer(games, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_a_game(self):
        """
        Test get details on a game.

        """
        game = create_game(self.user)

        url = reverse("game:game-detail", args=[game.game_id])
        response = self.client.get(url)

        serializer = GameSerializer(game)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_game_by_username_search(self) -> None:
        """
        Test retrieving a game by username search.

        """
        create_game(self.user)
        create_game(self.user)

        response = self.client.get(
            reverse("game:game-list"), {"search": self.user.username}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_user_game_history(self):
        """
        Test retrieving a user's game history.

        """

        create_game(self.user)
        create_game(self.user)

        response = self.client.get(reverse("game:game:game-history"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        response = self.client.get(reverse("game:game:game-history"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
