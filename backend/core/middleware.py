"""
File: middleware.py
Project: Backend - Connect Four
File Created: Sunday, 21st July 2024 11:50:14 AM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: Middleware to add the Guest Session ID to the response headers
-----
Last Modified: Sunday, 21st July 2024 12:50:54 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

import contextlib

from core.models import Guest
from django.urls import reverse


class GuestSessionIDMiddleware:
    """
    Middleware to add the Guest Session ID to the response headers

    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if (
            request.path == reverse("user:guest-create")
            and response.status_code == 201
            and request.method == "POST"
        ):
            if guest_session_id := self.get_guest_session_id(response):
                response["Guest-Session-ID"] = guest_session_id

        return response

    def get_guest_session_id(self, response):
        """
        Get the Guest Session ID from the response data

        """

        if guest_id := response.data.get("guest_id", None):
            with contextlib.suppress(Guest.DoesNotExist):
                guest = Guest.objects.get(guest_id=guest_id)
                return guest.session_id

        return None
