"""
File: models.py
Project: Backend - Connect Four
File Created: Thursday, 18th July 2024 12:18:44 PM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: The models for system.
-----
Last Modified: Saturday, 20th July 2024 6:08:38 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import (
    EmailValidator,
    MinLengthValidator,
    RegexValidator,
)
from django.db import models

username_validator = RegexValidator(
    regex="^[a-zA-Z0-9_]*$",
    message="Username must be alphanumeric or contain underscores only.",
)


def default_board():
    return [[0 for _ in range(7)] for _ in range(6)]


class UserManager(BaseUserManager):
    """
    Manager users in the system.
    """

    def create_user(self, username: str, password: str, **extra_fields):
        """
        Creates a new user with a specified username, password, and additional
        fields.

        Parameters
        ----------
        username : str
            The username of the user being created.

        password : Optional[str]
            The password of the user being created.

        Returns
        -------
            The `create_user` method returns the user object that has been
            created and saved in the database.

        """
        if not username:
            raise ValueError("User must have a username.")

        if not password:
            raise ValueError("User must have a password.")

        # Convert the username to lowercase
        username = username.lower()

        if email := extra_fields.get("email", None):
            email = self.normalize_email(email)
            extra_fields["email"] = email

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username: str, password: str):
        """
        Creates a new superuser with a specified username and password.

        Parameters
        ----------
        username : str
            The username of the superuser being created.

        password : str
            The password of the superuser being created.

        Returns
        -------
            The `create_superuser` method returns the superuser object that has
            been created and saved in the database.

        """

        return self.create_user(
            username,
            password,
            is_staff=True,
            is_superuser=True,
            is_adv_logs=True,
        )


class User(AbstractBaseUser, PermissionsMixin):
    """
    Users within the system are represented by this model.

    """

    user_id = models.UUIDField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        default=uuid.uuid4,
        editable=False,
    )

    username = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(5), username_validator],
    )
    email = models.EmailField(
        max_length=255, unique=True, validators=[EmailValidator()]
    )
    profile_picture = models.CharField(max_length=255, blank=True)
    is_auth_logs = models.BooleanField(default=True)
    is_adv_logs = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "username"

    def __str__(self) -> str:
        return f"{self.username}"


class Guest(models.Model):
    """
    Guests within the system are represented by this model.

    """

    guest_id = models.UUIDField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        default=uuid.uuid4,
        editable=False,
    )
    username = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(5), username_validator],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Define the parameters to display on the admin page for Guest.

        """

        ordering = ["guest_id"]
        verbose_name = "Guest"
        verbose_name_plural = "Guests"

    def __str__(self) -> str:
        return f"{self.username}"

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        super().save(*args, **kwargs)

    @property
    def is_authenticated(self):
        """
        Always return True. This method is used to identify if the user
        is authenticated in Django.
        """
        return True


class Algorithm(models.Model):
    """
    Algorithms within the system are represented by this model.

    """

    algorithm_id = models.UUIDField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Define the parameters to display on the admin page for Algorithm.

        """

        ordering = ["algorithm_id"]
        verbose_name = "Algorithm"
        verbose_name_plural = "Algorithms"

    def __str__(self) -> str:
        return f"{self.name}"


class Player(models.Model):
    """
    Represents players within the system.
    """

    player_id = models.UUIDField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        default=uuid.uuid4,
        editable=False,
    )

    # Relationships
    user = models.OneToOneField(
        User, on_delete=models.RESTRICT, null=True, blank=True
    )
    guest = models.OneToOneField(
        Guest, on_delete=models.RESTRICT, null=True, blank=True
    )
    algorithm = models.OneToOneField(
        Algorithm, on_delete=models.RESTRICT, null=True, blank=True
    )

    # Player attributes
    is_human = models.BooleanField(default=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    total_games = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return (
            self.user.username
            if self.user
            else self.guest.username
            if self.guest
            else self.algorithm.name
            if self.algorithm
            else str(self.player_id)
        )


class Status(models.Model):
    """
    Represents the status of a game.

    """

    status_id = models.UUIDField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Define the parameters to display on the admin page for Status.

        """

        ordering = ["status_id"]
        verbose_name_plural = "Statuses"
        db_table = "Statuses"

    def __str__(self) -> str:
        return f"{self.name}"


class Game(models.Model):
    """
    Represents a game within the system.
    """

    game_id = models.UUIDField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        default=uuid.uuid4,
        editable=False,
    )
    player_one = models.ForeignKey(
        Player,
        on_delete=models.RESTRICT,
        related_name="player_one",
        null=False,
        blank=False,
    )
    player_two = models.ForeignKey(
        Player,
        on_delete=models.RESTRICT,
        related_name="player_two",
        null=True,
        blank=True,
    )
    rows = models.IntegerField(default=6)
    columns = models.IntegerField(default=7)
    board = models.JSONField(default=default_board)
    status = models.ForeignKey(
        Status, on_delete=models.RESTRICT, null=True, blank=True
    )
    current_turn = models.ForeignKey(
        Player,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="current_turn",
    )
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    winner = models.ForeignKey(
        Player,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="winner",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Define the parameters to display on the admin page for Game.

        """

        ordering = ["game_id"]
        verbose_name = "Game"
        verbose_name_plural = "Games"

    def __str__(self) -> str:
        return f"{self.game_id}"
