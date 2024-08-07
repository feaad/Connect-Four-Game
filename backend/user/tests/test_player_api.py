from core.models import Algorithm, EloHistory, Guest, Player, User
from core.tests.helper import create_elo_history
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITransactionTestCase
from user.serializers import EloHistorySerializer, PlayerSerializer

PLAYER_URL = reverse("user:player-list")
ELO_URL = reverse("user:elohistory-list")


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
        self.guest = Guest.objects.create(username="test_guest")
        self.user = User.objects.create(
            username="test_user", password="test_password"
        )
        self.user_player = Player.objects.get(user=self.user)

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

        response = self.client.get(
            reverse("user:player-detail", args=[self.user_player.player_id])
        )

        serializer = PlayerSerializer(self.user_player)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_player_by_username_search(self) -> None:
        """
        Test retrieving a player by username search.

        """

        response = self.client.get(
            PLAYER_URL, {"search": self.user_player.user.username}
        )

        serializer = PlayerSerializer(self.user_player)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [serializer.data])

    def test_retrieve_elo_history(self) -> None:
        """
        Test retrieving a list of elo histories.

        """
        create_elo_history(self.user, 1500)
        create_elo_history(self.guest, 1500)

        response = self.client.get(ELO_URL)

        elo_histories = EloHistory.objects.all()
        serializer = EloHistorySerializer(elo_histories, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)

    def test_get_elo_history_by_id(self) -> None:
        """
        Test retrieving an elo history by id.

        """
        elo_history = create_elo_history(self.user, 1500)

        response = self.client.get(
            reverse(
                "user:elohistory-detail", args=[elo_history.elo_history_id]
            )
        )

        serializer = EloHistorySerializer(elo_history)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_elo_history_by_player_id(self) -> None:
        """
        Test retrieving an elo history by player id.

        """

        create_elo_history(self.user, 1500)
        create_elo_history(self.guest, 1500)

        response = self.client.get(
            ELO_URL, {"search": self.user_player.player_id}
        )

        elo_history = EloHistory.objects.get(player=self.user_player)
        serializer = EloHistorySerializer(elo_history)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [serializer.data])
