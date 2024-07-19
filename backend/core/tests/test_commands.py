"""
File: test_commands.py
Project: Backend - Connect Four
File Created: Thursday, 18th July 2024 6:20:40 PM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: Test the custom management commands.
-----
Last Modified: Friday, 19th July 2024 11:03:18 AM
Modified By: feaad
-----
Copyright ©2024 feaad
"""


from io import StringIO
from os import environ
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase
from psycopg import OperationalError as Psycopg2OpError


def call_cmd(cmd, *args, **kwargs) -> str:
    """
    Executes a command with specified arguments and returns the output as a
    string.

    Parameters
    ----------
    cmd
        Command to be executed.
    Returns
    -------
    str
        Output of the command.

    """
    out = StringIO()
    call_command(
        cmd,
        *args,
        stdout=out,
        stderr=StringIO(),
        **kwargs,
    )
    return out.getvalue()


@patch("core.management.commands.wait_for_db.Command.check")
class WaitForDBCommandTests(TestCase):
    """
    Test Database connections

    """

    def test_wait_for_db_ready(self, patched_check) -> None:
        """
        Unit Test for wait for database command until ready.

        """
        patched_check.return_value = True

        output = call_cmd("wait_for_db")

        # Assert the check method was called once
        patched_check.assert_called_once_with(databases=["default"])

        # Assert the success message was printed
        self.assertIn("Database available!", output)

    @patch("time.sleep", return_value=None)
    def test_wait_for_db_delay(self, patched_sleep, patched_check) -> None:
        """
        Unit Test for wait for database command with delay.

        """

        patched_check.side_effect = (
            [Psycopg2OpError] * 2 + [OperationalError] * 3 + [True]
        )
        output = call_cmd("wait_for_db")

        self.assertEqual(patched_check.call_count, 6)

        # Assert the warning message was printed
        self.assertIn("Database unavailable, waiting for a second...", output)


class InitSUCommandTests(TestCase):
    """
    Test the init_su command.

    """

    def setUp(self):
        """
        Set up environment variables.

        """
        self.env = patch.dict(
            "os.environ",
            {
                "SUPERUSER_USERNAME": "test_superuser",
                "SUPERUSER_PASSWORD": "password",
            },
        )

    def test_init_su(self):
        """
        Test Case for creating superuser.

        """
        with self.env:
            output = call_cmd("init_su")
            self.assertIn("Superuser created successfully.", output)

    def test_init_su_users_exist(self) -> None:
        """
        Test Case for creating superuser when users already exist.

        """
        get_user_model().objects.create_superuser("test_superuser", "password")
        with self.env:
            output = call_cmd("init_su")
            self.assertIn(
                "Superuser can only be initialized if none exists", output
            )

    def test_init_su_no_credentials(self) -> None:
        """
        Test Case for creating superuser with no environment variables.

        """
        with patch.dict("os.environ"):
            if "SUPERUSER_USERNAME" in environ:
                del environ["SUPERUSER_USERNAME"]

            if "SUPERUSER_PASSWORD" in environ:
                del environ["SUPERUSER_PASSWORD"]

            output = call_cmd("init_su")
            self.assertIn("Superuser credentials are missing.", output)
