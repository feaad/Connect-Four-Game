from random import choice
from typing import Optional, Union

from django.contrib.auth import get_user_model

from core import models
from core.utils import get_player_by_username


def create_user(
    username: str = "testuser",
    password: str = "password",
    email: str = "test@example.com",
) -> models.User:
    """
    Helper function to create a user.

    """

    return get_user_model().objects.create_user(
        username=username, password=password, email=email
    )


def create_guest(username: str = "test_guest") -> models.Guest:
    """
    Helper function to create a guest.

    """
    instance, _ = models.Guest.objects.get_or_create(username=username)

    return instance


def create_algorithm(
    name: str = "test_algorithm",
    description: str = "This is a test algorithm.",
) -> models.Algorithm:
    """
    Helper function to create an algorithm.

    """
    instance, _ = models.Algorithm.objects.get_or_create(
        name=name, description=description
    )

    return instance


def create_status(
    name: str = "test_status", description: str = "This is a test status."
) -> models.Status:
    """
    Helper function to create a status.

    """
    instance, _ = models.Status.objects.get_or_create(
        name=name, description=description
    )

    return instance


def create_game() -> models.Game:
    """
    Helper function to create a game.

    """
    player_one = create_user()
    player_two = create_guest()
    status = create_status()

    instance, _ = models.Game.objects.get_or_create(
        player_one=models.Player.objects.get(user=player_one),
        player_two=models.Player.objects.get(guest=player_two),
        status=status,
        current_turn=models.Player.objects.get(user=player_one),
        created_by=models.Player.objects.get(user=player_one),
    )

    return instance


def create_match_making() -> models.MatchMakingQueue:
    """
    Helper function to create a match making.

    """
    guest = create_guest()
    status = create_status("Queued", "The player is in the queue.")
    player = models.Player.objects.get(guest=guest)

    instance, _ = models.MatchMakingQueue.objects.get_or_create(
        player=player, status=status
    )

    return instance


def create_game_invitation(
    player_one: Optional[Union[models.Guest, models.User]] = None,
    player_two: Optional[Union[models.Guest, models.User]] = None,
) -> models.GameInvitation:
    """
    Helper function to create a game invitation.

    """
    player_one = create_user() if player_one is None else player_one
    player_two = create_guest() if player_two is None else player_two
    status = create_status("Pending")

    instance, _ = models.GameInvitation.objects.get_or_create(
        sender=get_player_by_username(player_one.username),
        receiver=get_player_by_username(player_two.username),
        play_preference=choice(["first", "second", "random"]),
        status=status,
    )

    return instance


def create_move(
    game: Optional[models.Game] = None,
    player: Optional[models.Player] = None,
    row: Optional[int] = 0,
    column: Optional[int] = 0,
) -> models.Move:
    """
    Helper function to create a move.

    """
    game = create_game() if game is None else game
    player = (
        models.Player.objects.get(user=create_user())
        if player is None
        else player
    )

    instance, _ = models.Move.objects.get_or_create(
        game=game, player=player, row=row, column=column
    )

    return instance
