"""
File: wait_for_db.py
Project: Backend - Connect Four
File Created: Thursday, 18th July 2024 1:01:44 PM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: Command to wait for the database to be available.
-----
Last Modified: Thursday, 18th July 2024 1:08:10 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""


import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg import OperationalError as Psycopg2OpError


class Command(BaseCommand):
    """
    Command to wait for the database to be available.

    """

    help = "Waits for the database to become available."

    def handle(self, *args, **options):
        """
        Handle the command.

        """

        self.stdout.write("Waiting for database...")
        db_conn = None

        while not db_conn:
            try:
                self.check(databases=["default"])
                db_conn = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write(
                    "Database unavailable, waiting for a second..."
                )
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
