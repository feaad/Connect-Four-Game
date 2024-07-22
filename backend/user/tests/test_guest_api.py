"""
File: test_guest_api.py
Project: Backend - Connect Four
File Created: Sunday, 21st July 2024 12:21:55 AM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: Test guest API endpoints.
-----
Last Modified: Sunday, 21st July 2024 1:49:46 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from core.models import Guest, Player
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

GUEST_URL = reverse("user:guest:guest-detail")
CREATE_GUEST_URL = reverse("user:guest:guest-create")
CONVERT_GUEST_URL = reverse("user:guest:guest-convert")

GUEST_PAYLOAD = {"username": "test_guest_user"}


def create_guest(**params):
    """
    Create a new guest

    """
    return Guest.objects.create(**params)


class PublicUserAPITests(APITestCase):
    """
    API Requests that do not require Authentication

    """

    def setUp(self):
        self.client = APIClient()

    def test_create_guest_success(self):
        """
        Test creating a new guest with a POST request.
        """

        response = self.client.post(CREATE_GUEST_URL, GUEST_PAYLOAD)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        guest = Guest.objects.get(username=GUEST_PAYLOAD["username"])

        player = Player.objects.get(guest=guest)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(player.guest, guest)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_create_guest_with_existing_username(self):
        """
        Test creating a guest with an existing username

        """

        create_guest(**GUEST_PAYLOAD)

        response = self.client.post(CREATE_GUEST_URL, GUEST_PAYLOAD)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

    def test_create_guest_with_existing_username_user_table(self):
        """
        Test creating a guest with an existing username in the user table

        """

        get_user_model().objects.create_user(
            username=GUEST_PAYLOAD["username"], password="testpassword"
        )

        response = self.client.post(CREATE_GUEST_URL, GUEST_PAYLOAD)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Username already exists")
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)


class PrivateUserAPITests(APITestCase):
    """
    API Requests that require Authentication

    """

    def setUp(self):
        self.client = APIClient()
        self.guest = create_guest(**GUEST_PAYLOAD)
        self.client.force_authenticate(user=self.guest)

    def test_retrieve_guest(self):
        """
        Test retrieving the authenticated guest

        """

        response = self.client.get(GUEST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["guest_id"], str(self.guest.guest_id))
        self.assertEqual(response.data["username"], self.guest.username)

    def test_update_guest(self):
        """
        Test updating the guest

        """

        payload = {"username": "new_guest_username"}

        response = self.client.patch(GUEST_URL, payload)

        self.guest.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], payload["username"])
        self.assertEqual(self.guest.username, payload["username"])
        self.assertNotEqual(self.guest.username, GUEST_PAYLOAD["username"])

    def test_update_guest_username_with_existing_username(self):
        """
        Test updating the guest with an existing username

        """

        create_guest(username="new_guest_username")

        payload = {"username": "new_guest_username"}

        response = self.client.patch(GUEST_URL, payload)

        self.guest.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unallowed_http_method(self):
        """
        Test an unallowed HTTP method

        """

        response = self.client.put(GUEST_URL)

        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_guest_registration(self):
        """
        Test guest registration

        """

        payload = {"email": "user@example.com", "password": "testpassword"}

        response = self.client.post(CONVERT_GUEST_URL, payload)

        user = get_user_model().objects.get(username=GUEST_PAYLOAD["username"])
        player = Player.objects.get(guest=self.guest)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(player.user, user)
        self.assertNotIn("password", response.data)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
