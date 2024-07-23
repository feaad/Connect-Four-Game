"""
File: serializers.py
Project: Backend - Connect Four
File Created: Saturday, 20th July 2024 4:13:33 PM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: Serializers for the core app.
-----
Last Modified: Saturday, 20th July 2024 4:18:23 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""


from app.settings import SIMPLE_JWT
from core.models import Guest, User
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken


class HealthCheckSerializer(serializers.Serializer):
    """
    Serializer for the health check endpoint.

    """

    healthy = serializers.BooleanField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        # Add additional data to the response
        if isinstance(user, Guest):
            data["guest_id"] = user.id
        elif isinstance(user, User):
            data["user_id"] = user.id

        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = RefreshToken(attrs["refresh"])
        user_id = refresh.get("user_id", None)
        guest_id = refresh.get("guest_id", None)

        if user_id:
            data["user_id"] = user_id
        if guest_id:
            data["guest_id"] = guest_id

        return data


class CustomTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        try:
            UntypedToken(attrs["token"])
        except TokenError as e:
            raise InvalidToken(e.args[0])

        validated_token = UntypedToken(attrs["token"])
        user_id_claim = SIMPLE_JWT.get("USER_ID_CLAIM", "user_id")
        guest_id_claim = "guest_id"

        if (
            user_id_claim not in validated_token
            and guest_id_claim not in validated_token
        ):
            raise InvalidToken(
                "Token contained no recognizable user or guest identification"
            )

        return {}
