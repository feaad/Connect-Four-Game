from core.models import Player, User


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
