"""
File: test_user_api.py
Project: Backend - Connect Four
File Created: Saturday, 20th July 2024 1:53:44 PM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: Test user API endpoints.
-----
Last Modified: Saturday, 20th July 2024 4:36:39 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from core.models import Guest, Player
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

REGISTER_USER_URL = reverse("user:user:user-register")
AUTH_LOGIN_URL = reverse("core:auth:login")
AUTH_LOGOUT_URL = reverse("core:auth:logout")
AUTH_LOGOUT_ALL_URL = reverse("core:auth:logout-all")
USER_DETAIL_URL = reverse("user:user:user-detail")

USER_PAYLOAD = {
    "username": "test_username",
    "email": "test@example.com",
    "password": "testpassword1234",
}


def create_user(**params):
    """
    Creates a new user

    """
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(APITestCase):
    """
    API Requests that do not require Authentication

    """

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """
        Test the creation of a new User

        """

        response = self.client.post(REGISTER_USER_URL, USER_PAYLOAD)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(username=USER_PAYLOAD["username"])
        self.assertTrue(user.check_password(USER_PAYLOAD["password"]))

        player = Player.objects.get(user=user)
        self.assertEqual(player.user, user)
        self.assertNotIn("password", response.data)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_create_user_with_invalid_email(self):
        """
        Test creating a user with an invalid email

        """

        payload = USER_PAYLOAD.copy()
        payload["email"] = "test"

        response = self.client.post(REGISTER_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_existing_username(self):
        """
        Test creating a user with an existing username

        """

        create_user(**USER_PAYLOAD)

        payload = USER_PAYLOAD.copy()
        payload["email"] = "test_2@example.com"

        response = self.client.post(REGISTER_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_existing_username_in_guest_table(self):
        """
        Test creating a user with an existing username in the guest table

        """

        Guest.objects.create(username=USER_PAYLOAD["username"])

        response = self.client.post(REGISTER_USER_URL, USER_PAYLOAD)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Username already exists")

    def test_create_user_with_existing_email(self):
        """
        Test creating a user with an existing email

        """
        create_user(**USER_PAYLOAD)

        payload = USER_PAYLOAD.copy()
        payload["username"] = "test_2"

        response = self.client.post(REGISTER_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_invalid_username(self):
        """
        Test creating a user with an invalid username

        """

        payload = USER_PAYLOAD.copy()
        payload["username"] = "te-st usern@me"
        response = self.client.post(REGISTER_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_no_email(self):
        """
        Test creating a user with no email

        """

        payload = USER_PAYLOAD.copy()
        payload.pop("email")

        response = self.client.post(REGISTER_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
        Test that the password is more than 8 characters

        """
        payload = USER_PAYLOAD.copy()
        payload["password"] = "pw"

        response = self.client.post(REGISTER_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = (
            get_user_model()
            .objects.filter(username=USER_PAYLOAD["username"])
            .exists()
        )
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """
        Test token generation for valid credentials

        """

        create_user(**USER_PAYLOAD)

        payload = {
            "username": USER_PAYLOAD["username"],
            "password": USER_PAYLOAD["password"],
        }
        response = self.client.post(AUTH_LOGIN_URL, payload)

        user = get_user_model().objects.get(username=USER_PAYLOAD["username"])
        token = OutstandingToken.objects.get(user=user)

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["refresh"], str(token.token))

    def test_create_token_for_wrong_password(self):
        """
        Test token generation for wrong password

        """

        create_user(**USER_PAYLOAD)

        payload = {
            "username": USER_PAYLOAD["username"],
            "password": "password",
        }
        response = self.client.post(AUTH_LOGIN_URL, payload)

        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)
        self.assertEqual(response.data["error"], "Wrong password")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_non_existent_user(self):
        """
        Test token generation for non-existent user

        """

        create_user(**USER_PAYLOAD)

        payload = {
            "username": "user",
            "password": USER_PAYLOAD["username"],
        }
        response = self.client.post(AUTH_LOGIN_URL, payload)

        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)
        self.assertEqual(response.data["error"], "No user exists")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_token_for_inactive_user(self):
        """
        Test token generation for inactive user

        """

        user = create_user(**USER_PAYLOAD)
        user.is_active = False
        user.save()

        payload = {
            "username": USER_PAYLOAD["username"],
            "password": USER_PAYLOAD["password"],
        }
        response = self.client.post(AUTH_LOGIN_URL, payload)

        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)
        self.assertEqual(response.data["error"], "User is not active")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """
        Test that authentication is required for users

        """
        response = self.client.get(USER_DETAIL_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(APITestCase):
    """
    API Requests that do require Authentication

    """

    def setUp(self):
        self.user = create_user(**USER_PAYLOAD)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_profile_success(self):
        """
        Test retrieving profile for logged in user

        """
        response = self.client.get(USER_DETAIL_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["email"], self.user.email)

    def test_update_user_profile(self):
        """
        Test updating user details

        """

        payload = {"profile_picture": "new/profile.jpg"}

        response = self.client.patch(USER_DETAIL_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(self.user.profile_picture, payload["profile_picture"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_username(self):
        """
        Test updating user username

        """

        payload = {"username": "new_username"}

        response = self.client.patch(USER_DETAIL_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Username cannot be updated")

    def test_user_logout(self):
        """
        Test user logout

        """

        auth_payload = USER_PAYLOAD.copy()
        auth_payload.pop("email")

        auth_response = self.client.post(AUTH_LOGIN_URL, auth_payload)

        refresh = auth_response.data["refresh"]

        payload = {"refresh": refresh}

        response = self.client.post(AUTH_LOGOUT_URL, payload)
        token = OutstandingToken.objects.get(user=self.user)
        token_blacklist = BlacklistedToken.objects.get(token=token)

        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertIsNotNone(token_blacklist)

    def test_user_logout_without_refresh_token(self):
        """
        Test user logout without refresh token

        """

        response = self.client.post(AUTH_LOGOUT_URL)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Refresh token is required")

    def test_user_logout_all(self):
        """
        Test user logout all

        """

        auth_payload = USER_PAYLOAD.copy()
        auth_payload.pop("email")

        auth_response = self.client.post(AUTH_LOGIN_URL, auth_payload)

        refresh = auth_response.data["refresh"]

        payload = {"refresh": refresh}

        response = self.client.post(AUTH_LOGOUT_ALL_URL, payload)
        token = OutstandingToken.objects.get(user=self.user)
        token_blacklist = BlacklistedToken.objects.get(token=token)

        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertIsNotNone(token_blacklist)

    def test_delete_user(self):
        """
        Test deleting a user

        """

        response = self.client.delete(USER_DETAIL_URL)

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data["message"], "User deleted")
        self.assertFalse(self.user.is_active)
