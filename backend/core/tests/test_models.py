"""
File: test_models.py
Project: Backend - Connect Four
File Created: Friday, 19th July 2024 10:26:59 AM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: Unit Testing for various models.
-----
Last Modified: Saturday, 20th July 2024 6:08:53 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""


from core import models
from django.contrib.auth import get_user_model
from django.test import TransactionTestCase

SAMPLE_USERNAMES = [
    ["tesT1", "test1"],
    ["Test2", "test2"],
    ["TEST3", "test3"],
    ["test4", "test4"],
]


def create_user(username: str = "testuser", password: str = "password"):
    """Create a user for testing purposes.

    Parameters
    ----------
    username : (str, optional)
        Username. Defaults to 'testuser'.

    password : (str, optional)
        Password. Defaults to 'password'.

    Returns
    -------
    User
        The user object that has been created and saved in the database.
    """
    return get_user_model().objects.create_user(username, password)


class ModelTests(TransactionTestCase):
    """
    Test Models.

    """

    def test_create_user_successful(self) -> None:
        """
        Test Case for creating a user with a username and password.

        """
        username = "testuser"
        password = "password"
        user = create_user(username, password)

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)

    def test_create_user_email_normalized(self) -> None:
        """
        Test Case for normalizing the email for a new user.

        """

        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for index, (email, expected) in enumerate(sample_emails):
            user = get_user_model().objects.create_user(
                username=f"test{index}",
                password="password",
                email=email,
            )
            self.assertEqual(user.email, expected)

    def test_create_user_username_normalized(self) -> None:
        """
        Test Case for normalizing the username for a new user.

        """

        for username, expected in SAMPLE_USERNAMES:
            user = get_user_model().objects.create_user(
                username=username,
                email=f"{username}@example.com",
                password="password",
            )
            self.assertEqual(user.username, expected)

    def test_create_user_unsuccessful(self) -> None:
        """
        Test Case for creating a user with no username or password.

        """

        # Test for no username
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

        # Test for no password
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                "user",
                "",
            )

    def test_create_superuser(self) -> None:
        """
        Test Case for creating a super user.

        """
        user = get_user_model().objects.create_superuser(
            "test_superuser", "password"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_guest(self) -> None:
        """
        Test Case for creating a guest.

        """
        guest_name = "test_guest"
        guest = models.Guest.objects.create(username=guest_name)

        self.assertEqual(guest.username, guest_name)
        self.assertIn(guest_name, str(guest))

    def test_create_guest_username_normalized(self) -> None:
        """
        Test Case for normalizing the username for a new guest.

        """

        for username, expected in SAMPLE_USERNAMES:
            guest = models.Guest.objects.create(username=username)
            self.assertEqual(guest.username, expected)
