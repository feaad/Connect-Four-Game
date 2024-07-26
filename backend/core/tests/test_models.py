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


import core.tests.helper as hp
from core import models
from core.constants import DEFAULT_COLUMNS, DEFAULT_ROWS
from django.contrib.auth import get_user_model
from django.test import TransactionTestCase

SAMPLE_USERNAMES = [
    ["tesT1", "test1"],
    ["Test2", "test2"],
    ["TEST3", "test3"],
    ["test4", "test4"],
]


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
        user = hp.create_user(username, password)

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
            user = hp.create_user(
                f"test{index}",
                "password",
                email,
            )
            self.assertEqual(user.email, expected)

    def test_create_user_username_normalized(self) -> None:
        """
        Test Case for normalizing the username for a new user.

        """

        for username, expected in SAMPLE_USERNAMES:
            user = hp.create_user(
                username=username,
                password="password",
                email=f"{username}@example.com",
            )
            self.assertEqual(user.username, expected)

    def test_create_user_unsuccessful(self) -> None:
        """
        Test Case for creating a user with no username or password.

        """

        # Test for no username
        with self.assertRaises(ValueError):
            hp.create_user("", "test123")

        # Test for no password
        with self.assertRaises(ValueError):
            hp.create_user(
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
        guest = hp.create_guest(guest_name)

        self.assertEqual(guest.username, guest_name)
        self.assertIn(guest_name, str(guest))

    def test_create_guest_username_normalized(self) -> None:
        """
        Test Case for normalizing the username for a new guest.

        """

        for username, expected in SAMPLE_USERNAMES:
            guest = hp.create_guest(username)
            self.assertEqual(guest.username, expected)

    def test_create_algorithm(self) -> None:
        """
        Test Case for creating an algorithm.

        """
        name = "test_algorithm"
        description = "This is a test algorithm."
        algorithm = hp.create_algorithm(name, description)

        self.assertEqual(algorithm.name, name)
        self.assertEqual(algorithm.description, description)

    def test_create_player_when_user_created(self) -> None:
        """
        Test Case for creating a player when a user is created.

        """
        user = hp.create_user()
        player = models.Player.objects.get(user=user)

        self.assertIsNotNone(player)
        self.assertEqual(player.user, user)
        self.assertTrue(player.is_human)

    def test_create_player_when_guest_created(self):
        """
        Test Case for creating a player when a guest is created.

        """
        guest = hp.create_guest()
        player = models.Player.objects.get(guest=guest)

        self.assertIsNotNone(player)
        self.assertEqual(player.guest, guest)
        self.assertTrue(player.is_human)

    def test_create_player_when_algorithm_created(self):
        """
        Test Case for creating a player when an algorithm is created.

        """
        algorithm = hp.create_algorithm()
        player = models.Player.objects.get(algorithm=algorithm)

        self.assertIsNotNone(player)
        self.assertEqual(player.algorithm, algorithm)
        self.assertFalse(player.is_human)

    def test_create_status(self) -> None:
        """
        Test Case for creating a status.

        """
        name = "test_status"
        description = "This is a test status."
        status = hp.create_status(name, description)

        self.assertEqual(status.name, name)
        self.assertEqual(status.description, description)

    def test_create_game(self) -> None:
        """
        Test Case for creating a game.

        """

        game = hp.create_game()

        self.assertIsNotNone(game)
        self.assertEqual(game.player_one.user.username, "testuser")
        self.assertEqual(game.player_two.guest.username, "test_guest")
        self.assertEqual(game.status.name, "test_status")
        self.assertEqual(game.rows, DEFAULT_ROWS)
        self.assertEqual(game.columns, DEFAULT_COLUMNS)

    def test_create_match_making(self) -> None:
        """
        Test Case for creating a match making.

        """

        match_making = hp.create_match_making()

        self.assertIsNotNone(match_making)
        self.assertEqual(match_making.player.guest.username, "test_guest")
        self.assertEqual(match_making.status.name, "Queued")
        self.assertIsNone(match_making.game)
