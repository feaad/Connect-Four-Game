"""
File: views.py
Project: Backend - Connect Four
File Created: Thursday, 18th July 2024 12:18:44 PM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: Core views for the system.
-----
Last Modified: Thursday, 18th July 2024 6:05:19 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""


from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health_check(request) -> Response:
    """
    Checks if Connect Four is healthy.

    """
    return Response({"healthy": True})
