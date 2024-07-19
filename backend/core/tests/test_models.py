"""
File: test_models.py
Project: Backend - Connect Four
File Created: Friday, 19th July 2024 10:26:59 AM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: Unit Testing for various models.
-----
Last Modified: Friday, 19th July 2024 10:37:42 AM
Modified By: feaad
-----
Copyright ©2024 feaad
"""


from django.contrib.auth import get_user_model
from django.test import TransactionTestCase


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
