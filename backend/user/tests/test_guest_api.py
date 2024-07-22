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

CREATE_GUEST_URL = reverse("user:guest-create")

GUEST_PAYLOAD = {"username": "test_guest_user"}


def create_guest(**params):
    """
    Create a new guest

    """
    return Guest.objects.create(**params)


def detail_url(guest_id):
    """
    Return the guest detail URL

    """
    return reverse("user:guest-detail", args=[guest_id])


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

        guest = Guest.objects.get(guest_id=response.data["guest_id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Guest-Session-ID", response.headers)
        self.assertEqual(
            str(guest.session_id), response.headers["Guest-Session-ID"]
        )
        self.assertEqual(guest.username, GUEST_PAYLOAD["username"])

    def test_create_guest_with_existing_username(self):
        """
        Test creating a guest with an existing username

        """

        create_guest(**GUEST_PAYLOAD)

        response = self.client.post(CREATE_GUEST_URL, GUEST_PAYLOAD)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("Guest-Session-ID", response.headers)
        self.assertNotIn("guest_id", response.data)

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
        self.assertNotIn("Guest-Session-ID", response.headers)
        self.assertNotIn("guest_id", response.data)


class PrivateUserAPITests(APITestCase):
    """
    API Requests that require Authentication

    """

    def setUp(self):
        self.client = APIClient()

        self.guest = create_guest(**GUEST_PAYLOAD)

        self.url = detail_url(self.guest.guest_id)
        self.header = {"Guest-Session-ID": self.guest.session_id}

    def test_retrieve_guest(self):
        """
        Test retrieving the authenticated guest

        """

        response = self.client.get(self.url, headers=self.header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["guest_id"], str(self.guest.guest_id))
        self.assertEqual(response.data["username"], self.guest.username)

    def test_retrieve_guest_without_permission(self):
        """
        Test retrieving the guest without permission

        """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn("guest_id", response.data)
        self.assertNotIn("username", response.data)

    def test_update_guest(self):
        """
        Test updating the guest

        """

        payload = {"username": "new_guest_username"}

        response = self.client.patch(self.url, payload, headers=self.header)

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

        response = self.client.patch(self.url, payload, headers=self.header)

        self.guest.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unallowed_http_method(self):
        """
        Test an unallowed HTTP method

        """

        response = self.client.put(self.url, headers=self.header)

        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_guest_registration(self):
        """
        Test guest registration

        """

        url = reverse("user:guest-register", args=[self.guest.guest_id])
        payload = {"email": "user@example.com", "password": "testpassword"}

        response = self.client.post(url, payload, headers=self.header)

        user = get_user_model().objects.get(username=GUEST_PAYLOAD["username"])
        player = Player.objects.get(guest=self.guest)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(player.user, user)
        self.assertNotIn("password", response.data)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
