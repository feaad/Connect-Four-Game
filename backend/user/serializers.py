from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User Object
    """

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
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
