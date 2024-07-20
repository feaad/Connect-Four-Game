from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

REGISTER_USER_URL = reverse("user:user-register")
AUTH_LOGIN_URL = reverse("login")
USER_DETAIL_URL = reverse("user:user-detail")

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


class PublicUserAPITests(TestCase):
    """
    API Requests that do not require Authentication

    """

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """
        Test the creation of a new User

        """

        res = self.client.post(REGISTER_USER_URL, USER_PAYLOAD)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(username=USER_PAYLOAD["username"])
        self.assertTrue(user.check_password(USER_PAYLOAD["password"]))

        self.assertNotIn("password", res.data)

    def test_create_user_with_existing_username(self):
        """
        Test creating a user with an existing username

        """

        create_user(**USER_PAYLOAD)

        payload = USER_PAYLOAD.copy()
        payload["email"] = "test_2@example.com"

        res = self.client.post(REGISTER_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_existing_email(self):
        """
        Test creating a user with an existing email

        """
        create_user(**USER_PAYLOAD)

        payload = USER_PAYLOAD.copy()
        payload["username"] = "test_2"

        res = self.client.post(REGISTER_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
        Test that the password is more than 8 characters

        """
        payload = USER_PAYLOAD.copy()
        payload["password"] = "pw"

        res = self.client.post(REGISTER_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
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
        res = self.client.post(AUTH_LOGIN_URL, payload)

        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_for_wrong_password(self):
        """
        Test token generation for wrong password

        """

        create_user(**USER_PAYLOAD)

        payload = {
            "username": USER_PAYLOAD["username"],
            "password": "password",
        }
        res = self.client.post(AUTH_LOGIN_URL, payload)

        self.assertNotIn("access", res.data)
        self.assertNotIn("refresh", res.data)
        self.assertEqual("Wrong password", res.data["error"])
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_non_existent_user(self):
        """
        Test token generation for non-existent user

        """

        create_user(**USER_PAYLOAD)

        payload = {
            "username": "user",
            "password": USER_PAYLOAD["username"],
        }
        res = self.client.post(AUTH_LOGIN_URL, payload)

        self.assertNotIn("access", res.data)
        self.assertNotIn("refresh", res.data)
        self.assertEqual("No user exists", res.data["error"])
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

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
        res = self.client.post(AUTH_LOGIN_URL, payload)

        self.assertNotIn("access", res.data)
        self.assertNotIn("refresh", res.data)
        self.assertEqual("User is not active", res.data["error"])
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """
        Test that authentication is required for users

        """
        res = self.client.get(USER_DETAIL_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
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
        res = self.client.get(USER_DETAIL_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["username"], self.user.username)
        self.assertEqual(res.data["email"], self.user.email)

    def test_update_user_profile(self):
        """
        Test updating user details

        """

        payload = {"profile_picture": "new/profile.jpg"}

        res = self.client.patch(USER_DETAIL_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(self.user.profile_picture, payload["profile_picture"])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
