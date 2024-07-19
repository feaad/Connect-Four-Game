"""Unit Test for the wait for database function."""
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase
from psycopg import OperationalError as Psycopg2OpError


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

        out = StringIO()
        call_command("wait_for_db", stdout=out)

        # Assert the check method was called once
        patched_check.assert_called_once_with(databases=["default"])

        # Assert the success message was printed
        self.assertIn("Database available!", out.getvalue())

    @patch("time.sleep", return_value=None)
    def test_wait_for_db_delay(self, patched_sleep, patched_check) -> None:
        """
        Unit Test for wait for database command with delay.

        """

        patched_check.side_effect = (
            [Psycopg2OpError] * 2 + [OperationalError] * 3 + [True]
        )
        out = StringIO()
        call_command("wait_for_db", stdout=out)

        self.assertEqual(patched_check.call_count, 6)

        # Assert the warning message was printed
        self.assertIn(
            "Database unavailable, waiting for a second...", out.getvalue()
        )
