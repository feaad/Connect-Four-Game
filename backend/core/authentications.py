from app.settings import SIMPLE_JWT
from core.models import Guest, User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_id_claim = SIMPLE_JWT.get("USER_ID_CLAIM", "user_id")
        guest_id_claim = "guest_id"

        # Attempt to retrieve a regular user
        user_id = validated_token.get(user_id_claim)
        if user_id is not None:
            try:
                return User.objects.get(pk=user_id)
            except ObjectDoesNotExist as e:
                raise InvalidToken(
                    f"No user found for user_id: {user_id}"
                ) from e

        # Attempt to retrieve a guest
        guest_id = validated_token.get(guest_id_claim)
        if guest_id is not None:
            try:
                return Guest.objects.get(pk=guest_id)
            except ObjectDoesNotExist as exc:
                raise InvalidToken(
                    f"No guest found for guest_id: {guest_id}"
                ) from exc

        # If neither user nor guest IDs are found in the token
        raise InvalidToken(
            "Token contained no recognizable user or guest identification"
        )
