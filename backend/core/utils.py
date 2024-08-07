from core.models import Player, User
from django.db.models import Q


def get_player(user):
    try:
        if hasattr(user, "guest_id"):
            return Player.objects.get(guest=user.guest_id)
        elif hasattr(user, "user_id"):
            u = User.objects.get(user_id=user.user_id)

            if not u.is_staff:
                return Player.objects.get(user=user.user_id)
    except (Player.DoesNotExist, User.DoesNotExist):
        return None

    return None


def get_username_or_name(player: Player) -> str:
    """
    Helper method to get the username or name from a Player object.
    """
    if player is None:
        return None
    if player.user:
        return player.user.username
    elif player.guest:
        return player.guest.username
    elif player.algorithm:
        return player.algorithm.code_name
    return ""


def get_player_by_username(username: str) -> Player | None:
    """
    Get a player by their username.
    """

    try:
        if player := Player.objects.get(
            Q(user__username=username) | Q(guest__username=username)
        ):
            return player
    except Player.DoesNotExist:
        return None

    return None
