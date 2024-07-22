from core.models import Algorithm, Guest, Player, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITransactionTestCase
from user.serializers import PlayerSerializer

PLAYER_URL = reverse("user:player-list")


class PublicUserAPITests(APITransactionTestCase):
    """
    API Requests that do not require Authentication.

    """

    def setUp(self) -> None:
        """Initialize an instance of APIClient."""
        self.client = APIClient()
        Algorithm.objects.create(
            name="test_algorithm", description="This is a test algorithm."
        )
        Guest.objects.create(username="test_guest")
        self.user = User.objects.create(
            username="test_user", password="test_password"
        )

    def test_retrieve_player(self) -> None:
        """
        Test retrieving a list of players.

        """

        response = self.client.get(PLAYER_URL)

        players = (
            Player.objects.all().filter(is_human=True).order_by("player_id")
        )
        serializer = PlayerSerializer(players, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)

    def test_get_player_by_id(self) -> None:
        """
        Test retrieving a player by id.

        """

        player = Player.objects.get(user=self.user)
        response = self.client.get(
            reverse("user:player-detail", args=[player.player_id])
        )

        serializer = PlayerSerializer(player)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_player_by_username_search(self) -> None:
        """
        Test retrieving a player by username search.

        """

        player = Player.objects.get(user=self.user)
        response = self.client.get(
            PLAYER_URL, {"search": player.user.username}
        )

        serializer = PlayerSerializer(player)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [serializer.data])
