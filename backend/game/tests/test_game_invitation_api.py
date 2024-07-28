from core.models import GameInvitation
from core.tests.helper import (
    create_game_invitation,
    create_guest,
    create_status,
    create_user,
)
from django.urls import reverse
from game.serializers import GameInvitationSerializer
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

INVITATION_URL = reverse("game:invitation-list")


def detail_url(invitation_id) -> str:
    """
    Return invitation detail URL.

    """
    return reverse("game:invitation-detail", args=[invitation_id])


def accept_url(invitation_id) -> str:
    """
    Return invitation accept URL.

    """
    return reverse("game:invitation-accept", args=[invitation_id])


def reject_url(invitation_id) -> str:
    """
    Return invitation reject URL.

    """
    return reverse("game:invitation-reject", args=[invitation_id])


class PrivateUserAPITests(APITestCase):
    """
    API Requests that do require Authentication

    """

    def setUp(self) -> None:
        self.user = create_user("username", email="username@example.com")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        create_status("Pending")
        create_status("Accepted")
        create_status("Created")
        create_status("Rejected")

    def test_retrieve_game_invitations(self) -> None:
        """
        Test retrieving a list of game invitations.

        """

        create_game_invitation(self.user)
        create_game_invitation(self.user, create_guest("my_guest"))

        response = self.client.get(INVITATION_URL)

        games = GameInvitation.objects.all().order_by("created_at")
        serializer = GameInvitationSerializer(games, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_game_invitations_with_no_invitations(self) -> None:
        """
        Test retrieving a list of game invitations with no invitations.

        """
        create_game_invitation(
            create_user("my_user", email="mysemail@email.com")
        )

        response = self.client.get(INVITATION_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_retrieve_game_invitation(self) -> None:
        """
        Test retrieving a game invitation.

        """

        game_invitation = create_game_invitation(self.user)

        response = self.client.get(detail_url(game_invitation.pk))

        serializer = GameInvitationSerializer(game_invitation)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_game_invitation_of_other_user(self) -> None:
        """
        Test retrieving a game invitation of other user.

        """

        game_invitation = create_game_invitation(
            create_user("my_user", email="mysemail@email.com")
        )

        response = self.client.get(detail_url(game_invitation.pk))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_game_invitation(self) -> None:
        """
        Test creating a game invitation.

        """

        create_guest("my_guest")
        payload = {"receiver": "my_guest"}

        response = self.client.post(INVITATION_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_game_invitation_with_unknown_receiver(self) -> None:
        """
        Test creating a game invitation with unknown receiver.

        """

        payload = {"receiver": "my_guest"}

        response = self.client.post(INVITATION_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Not a valid receiver")

    def test_create_game_invitation_with_no_receiver(self) -> None:
        """
        Test creating a game invitation with no receiver.

        """

        payload = {"receiver": ""}

        response = self.client.post(INVITATION_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Receiver are required.")

    def test_create_game_invitation_with_self_invite(self) -> None:
        """
        Test creating a game invitation with self invite.

        """

        payload = {"receiver": "username"}

        response = self.client.post(INVITATION_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "You can't invite yourself.")

    def test_create_game_invitation_with_invalid_play_preference(self) -> None:
        """
        Test creating a game invitation with invalid play preference.

        """

        create_guest("my_guest")
        payload = {"receiver": "my_guest", "play_preference": "invalid"}

        response = self.client.post(INVITATION_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Choose from ['first', 'second', 'random']"
        )

    def test_create_game_invitation_with_invalid_rows(self) -> None:
        """
        Test creating a game invitation with invalid rows.

        """

        create_guest("my_guest")

        payload = {"receiver": "my_guest", "rows": 0}

        response = self.client.post(INVITATION_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Rows and Columns must be at least 4"
        )

    def test_game_invitation_acceptance(self) -> None:
        """
        Test accepting a game invitation.

        """

        game_invitation = create_game_invitation(player_two=self.user)

        response = self.client.post(accept_url(game_invitation.invitation_id))

        game_invitation.refresh_from_db()
        serializer = GameInvitationSerializer(game_invitation)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(game_invitation.status.name, "Accepted")
        self.assertEqual(response.data, serializer.data)

    def test_game_invitation_acceptance_invalid_id(self) -> None:
        """
        Test accepting a game invitation with invalid id.

        """

        response = self.client.post(accept_url("jfuwhnudaww"))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["error"],
            "Game Invitation does not exist",
        )

    def test_game_invitation_acceptance_not_receiver(self) -> None:
        """
        Test creating a game invitation with invalid rows.

        """

        game_invitation = create_game_invitation()

        response = self.client.post(accept_url(game_invitation.invitation_id))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"],
            "You are not the receiver of this invitation",
        )

    def test_game_invitation_rejection(self) -> None:
        """
        Test rejecting a game invitation.

        """

        game_invitation = create_game_invitation(player_two=self.user)

        response = self.client.post(reject_url(game_invitation.invitation_id))

        game_invitation.refresh_from_db()
        serializer = GameInvitationSerializer(game_invitation)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(game_invitation.status.name, "Rejected")
        self.assertEqual(response.data, serializer.data)

    def test_game_invitation_rejection_invalid_id(self) -> None:
        """
        Test rejecting a game invitation with invalid id.

        """

        response = self.client.post(reject_url("jfuwhnudaww"))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["error"],
            "Game Invitation does not exist",
        )

    def test_game_invitation_rejection_not_receiver(self) -> None:
        """
        Test rejecting a game invitation with invalid rows.

        """

        game_invitation = create_game_invitation()

        response = self.client.post(reject_url(game_invitation.invitation_id))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"],
            "You are not the receiver of this invitation",
        )
