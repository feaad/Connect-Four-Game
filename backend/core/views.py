"""
File: views.py
Project: Backend - Connect Four
File Created: Thursday, 18th July 2024 12:18:44 PM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: Core views for the system.
-----
Last Modified: Saturday, 20th July 2024 4:17:27 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from core.serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
    CustomTokenVerifySerializer,
    HealthCheckSerializer,
)
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


class HealthCheckView(APIView):
    """
    Checks if Connect Four is healthy.
    """

    serializer_class = HealthCheckSerializer

    def get(self, _: Request) -> Response:
        """
        Get request to check if Connect Four is healthy.

        Parameters
        ----------
        request : Request
            The request object.

        Returns
        -------
        Response
            The response object.

        """

        serializer = self.serializer_class(data={"healthy": True})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


class CustomTokenVerifyView(TokenVerifyView):
    serializer_class = CustomTokenVerifySerializer
