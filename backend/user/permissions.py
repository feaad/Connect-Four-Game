"""
File: permissions.py
Project: Backend - Connect Four
File Created: Sunday, 21st July 2024 8:07:11 AM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: The permissions for the user app.
-----
Last Modified: Sunday, 21st July 2024 8:07:33 AM
Modified By: feaad
-----
Copyright ©2024 feaad
"""


from core.models import Guest
from django.urls import reverse
from rest_framework.permissions import BasePermission


class GuestHasSessionID(BasePermission):
    """
    Permission class to check if a guest has a session ID

    """

    def has_permission(self, request, view) -> bool:
        """
        Check if the guest has a session ID
        """

        # Allow the request if it's a POST request (creating a new guest)
        if request.method == "POST" and request.path == reverse(
            "user:guest-create"
        ):
            return True

        session_id = request.headers.get("Guest-Session-ID")

        if request.path.endswith("register"):
            guest_id = view.kwargs.get("guest_id")
        else:
            guest_id = view.kwargs.get("pk")

        if not guest_id or not session_id:
            return False

        try:
            Guest.objects.get(guest_id=guest_id, session_id=session_id)
        except Exception:
            return False

        return True
