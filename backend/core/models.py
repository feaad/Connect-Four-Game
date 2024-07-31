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

from core.constants import DEFAULT_COLUMNS, DEFAULT_ROWS, EMPTY
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
    regex="^[a-z0-9_]*$",
    message="Username must contain only lowercase alphanumeric & underscores.",
)

PLAY_PREFERENCE_CHOICES = [
    ("first", "First"),
    ("second", "Second"),
    ("random", "Random"),
]


def default_board():
    return [
        [EMPTY for _ in range(DEFAULT_COLUMNS)] for _ in range(DEFAULT_ROWS)
    ]


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
    elo = models.IntegerField(default=1200)
    last_activity = models.DateTimeField(null=True, blank=True)

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
    )
    player_two = models.ForeignKey(
        Player,
        on_delete=models.RESTRICT,
        related_name="player_two",
    )
    rows = models.IntegerField(default=DEFAULT_ROWS)
    columns = models.IntegerField(default=DEFAULT_COLUMNS)
    board = models.JSONField(default=default_board)
    status = models.ForeignKey(
        Status,
        on_delete=models.RESTRICT,
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
    created_by = models.ForeignKey(
        Player,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="created_by",
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


class MatchMakingQueue(models.Model):
    """
    Represents the Match Making Queue within the system.
    """

    queue_id = models.UUIDField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        default=uuid.uuid4,
        editable=False,
    )
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.RESTRICT,
    )
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Define the parameters to display on the admin page for
        MatchMakingQueue.

        """

        ordering = ["queue_id"]
        verbose_name = "Match Making Queue"
        verbose_name_plural = "Match Making Queues"

    def __str__(self) -> str:
        return f"{self.queue_id}"


class GameInvitation(models.Model):
    """
    Represents the Game Invitation within the system.
    """

    invitation_id = models.UUIDField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        default=uuid.uuid4,
        editable=False,
    )
    sender = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="sender"
    )
    receiver = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="receiver"
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.RESTRICT,
    )
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, null=True, blank=True
    )
    play_preference = models.CharField(
        max_length=10, choices=PLAY_PREFERENCE_CHOICES, default="random"
    )
    rows = models.IntegerField(default=DEFAULT_ROWS)
    columns = models.IntegerField(default=DEFAULT_COLUMNS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Define the parameters to display on the admin page for
        GameInvitation.

        """

        ordering = ["invitation_id"]
        verbose_name = "Game Invitation"
        verbose_name_plural = "Game Invitations"

    def __str__(self) -> str:
        return f"{self.invitation_id}"


class Move(models.Model):
    """
    Represents the Move within the system.
    """

    move_id = models.UUIDField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        default=uuid.uuid4,
        editable=False,
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(
        Player,
        on_delete=models.RESTRICT,
    )
    row = models.IntegerField()
    column = models.IntegerField()
    is_undone = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Define the parameters to display on the admin page for Move.

        """

        ordering = ["move_id"]
        verbose_name = "Move"
        verbose_name_plural = "Moves"

    def __str__(self) -> str:
        return f"{self.move_id}"


class EloHistory(models.Model):
    """
    Represents the Elo History within the system.
    """

    elo_history_id = models.UUIDField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        default=uuid.uuid4,
        editable=False,
    )
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    old_elo = models.IntegerField()
    new_elo = models.IntegerField()
    delta = models.IntegerField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Define the parameters to display on the admin page for EloHistory.

        """

        ordering = ["elo_history_id"]
        verbose_name = "Elo History"
        verbose_name_plural = "Elo Histories"

    def __str__(self) -> str:
        return f"{self.new_elo}-{self.old_elo}=({self.delta})"

    def save(self, *args, **kwargs):
        # Calculate the change in ELO before saving
        self.delta = self.new_elo - self.old_elo
        super().save(*args, **kwargs)
