"""
File: init_su.py
Project: Backend - Connect Four
File Created: Thursday, 18th July 2024 12:21:31 PM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: Command to create a superuser if one does not already exist.
-----
Last Modified: Thursday, 18th July 2024 1:08:27 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from decouple import config
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    """
    Command to create a superuser if one does not already exist.

    """

    help = "Creates a superuser if one does not already exist."

    def handle(self, *args, **options):
        """
        Handle the command.

        """

        password = config("SUPERUSER_PASSWORD", default="")
        username = config("SUPERUSER_USERNAME", default="")

        if not username or not password:
            self.stdout.write(
                self.style.WARNING("Superuser credentials are missing.")
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(
                    "Superuser can only be initialized if none exists"
                )
            )
        else:
            User.objects.create_superuser(username=username, password=password)
            self.stdout.write(
                self.style.SUCCESS("Superuser created successfully.")
            )
