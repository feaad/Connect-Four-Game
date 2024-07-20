"""
File: views.py
Project: Backend - Connect Four
File Created: Friday, 19th July 2024 12:16:25 PM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: The views for the user app.
-----
Last Modified: Saturday, 20th July 2024 11:17:38 AM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from core.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from user.serializers import UserSerializer


class RegisterView(GenericAPIView):
    """
    Register user view

    """

    serializer_class = UserSerializer

    def post(self, request: Request) -> Response:
        """
        Post request to register user

        Parameters
        ----------
        request : Request
            The request object.

        Returns
        -------
        Response
            The response object.

        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    """
    Login user view

    """

    serializer_class = UserSerializer

    def post(self, request: Request) -> Response:
        """
        Post request to login user

        Parameters
        ----------
        request : Request
            The request object.

        Returns
        -------
        Response
            The response object.
        """

        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(username=username)
            if not user.is_active:
                return Response(
                    {"error": "User is not active"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception:
            return Response(
                {"error": "No user exists"}, status=status.HTTP_404_NOT_FOUND
            )

        user = authenticate(
            request._request, username=username, password=password
        )
        if user is not None:
            login(request._request, user)
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Wrong password"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class LogoutView(GenericAPIView):
    """
    Logout user view

    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        Post request to logout user

        Parameters
        ----------
        request : Request
            The request object.

        Returns
        -------
        Response
            The response object.

        """
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request._request)
            return Response(
                {"message": "Logged out successfully"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class UserDetailView(GenericAPIView):
    """
    Retrieve and update user details view

    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """
        Retrieve user details.

        Parameters
        ----------
        request : Request
            The request object.

        Returns
        -------
        Response
            The response object.
        """
        user = request.user
        serializer = UserSerializer(user)

        return Response(serializer.data)

    def patch(self, request: Request) -> Response:
        """
        Update user details.

        Parameters
        ----------
        request : Request
            The request object.

        Returns
        -------
        Response
            The response object.
        """
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)