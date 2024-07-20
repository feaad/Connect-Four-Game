"""
File: models.py
Project: Backend - Connect Four
File Created: Thursday, 18th July 2024 12:18:44 PM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: The models for system.
-----
Last Modified: Thursday, 18th July 2024 1:20:43 PM
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
from django.core.validators import EmailValidator, MinLengthValidator
from django.db import models


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

        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Users within the system are represented by this model.

    """

    user_id = models.UUIDField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        default=uuid.uuid4,
    )

    username = models.CharField(
        max_length=50, unique=True, validators=[MinLengthValidator(5)]
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
