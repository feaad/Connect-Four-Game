from core.models import Player
from core.tests.helper import create_user
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

UPDATE_URL = reverse("user:update-activity")


class PublicUserAPITests(APITestCase):
    """
    API Requests that do not require Authentication

    """

    def setUp(self):
        self.client = APIClient()

    def test_update_activity_unauthorized(self):
        """
        Test that the user cannot update their activity without authentication

        """
        response = self.client.post(UPDATE_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(APITestCase):
    """
    API Requests that do require Authentication

    """

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_update_activity(self):
        """
        Test that the user can update their activity

        """
        player = Player.objects.get(user=self.user)
        self.assertEqual(player.last_activity, None)

        response = self.client.post(UPDATE_URL)

        player.refresh_from_db()

        self.assertNotEqual(player.last_activity, None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Activity updated")

    def test_update_activity_invalid_player(self):
        """
        Test that the user cannot update their activity if they do not have a
        player

        """
        player = Player.objects.get(user=self.user)
        player.delete()

        response = self.client.post(UPDATE_URL)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Player does not exist")
