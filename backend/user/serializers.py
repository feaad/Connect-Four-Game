"""
File: serializers.py
Project: Backend - Connect Four
File Created: Friday, 19th July 2024 12:47:19 PM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: Serializers for the user app.
-----
Last Modified: Saturday, 20th July 2024 4:18:46 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from core import models
from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User Object
    """

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        """
        Meta class for the GuestSerializer

        """

        model = get_user_model()
        fields = [
            "username",
            "password",
            "email",
            "profile_picture",
            "is_auth_logs",
            "is_adv_logs",
        ]

    def validate_email(self, value):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        return value.lower().strip()

    def create(self, validated_data):
        """
        Create user and encrypt password
        """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Update user details

        """
        validated_data.pop("username", None)

        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class GuestSerializer(serializers.ModelSerializer):
    """
    Serializer for the Guest Object
    """

    class Meta:
        """
        Meta class for the GuestSerializer

        """

        model = models.Guest
        fields = ["guest_id", "username"]
        read_only_fields = ["guest_id"]


class PlayerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Player Object
    """

    username = serializers.SerializerMethodField()
    is_guest = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class for the PlayerSerializer

        """

        model = models.Player
        fields = [
            "player_id",
            "username",
            "is_guest",
            "wins",
            "losses",
            "draws",
            "total_games",
            "elo",
            "last_activity",
        ]
        read_only_fields = [
            "player_id",
            "wins",
            "losses",
            "draws",
            "total_games",
            "elo",
            "last_activity",
        ]

    def get_username(self, obj: models.Player) -> str:
        if obj.user:
            return obj.user.username
        elif obj.guest:
            return obj.guest.username
        return None

    def get_is_guest(self, obj: models.Player) -> bool:
        return obj.user is None and obj.guest is not None


class UpdateActivitySerializer(serializers.Serializer):
    """
    Serializer for the UpdateActivityView
    """

    pass
