from core import models
from django.contrib.auth import get_user_model


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
