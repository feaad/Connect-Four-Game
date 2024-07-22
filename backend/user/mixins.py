"""
File: mixins.py
Project: Backend - Connect Four
File Created: Saturday, 20th July 2024 7:08:09 PM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: Mixin to handle authentication tasks.
-----
Last Modified: Saturday, 20th July 2024 7:28:20 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""


from rest_framework_simplejwt.tokens import RefreshToken


class AuthMixin:
    """
    Mixin to handle authentication tasks.
    """

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def get_tokens_for_guest(self, guest):
        guest_id_str = str(guest.guest_id)
        refresh = RefreshToken()
        access = refresh.access_token

        for token in (refresh, access):
            token["guest_id"] = guest_id_str

        return {
            "refresh": str(refresh),
            "access": str(access),
        }
