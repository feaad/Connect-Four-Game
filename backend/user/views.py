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


from core.constants import BACKENDS
from core.models import EloHistory, Guest, Player, User
from core.permissions import IsAuthenticatedGuest
from core.utils import get_player
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework_simplejwt.tokens import RefreshToken
from user.serializers import (
    EloHistorySerializer,
    GuestSerializer,
    PlayerSerializer,
    UpdateActivitySerializer,
    UserSerializer,
)

from .mixins import AuthMixin


class RegisterView(GenericAPIView, AuthMixin):
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

        # Check if username exists in guest table
        if Guest.objects.filter(
            username=request.data.get("username")
        ).exists():
            return Response(
                {"error": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if serializer.is_valid():
            user = serializer.save()
            tokens = self.get_tokens_for_user(user)
            # TODO: Send welcome email with custom template with celery
            return Response(tokens, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView, AuthMixin):
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

        username = request.data.get("username").lower()
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
            tokens = self.get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
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

            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

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


class LogoutAllView(GenericAPIView):
    """
    Logout all user view

    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        Post request to logout all user

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
            user = request.user
            tokens = OutstandingToken.objects.filter(user_id=user.user_id)
            for token in tokens:
                t, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response(
                {"message": "Logged out from all devices"},
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
        if "username" in request.data:
            return Response(
                {"error": "Username cannot be updated"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request) -> Response:
        """
        Delete user.

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
        user.is_active = False
        user.save()

        return Response(
            {"message": "User deleted"},
            status=status.HTTP_200_OK
        )


class RegisterGuestView(GenericAPIView, AuthMixin):
    """
    View for the Register Guest view
    """

    serializer_class = GuestSerializer

    def post(self, request: Request) -> Response:
        """
        Post request to register guest

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

        if User.objects.filter(username=request.data.get("username")).exists():
            return Response(
                {"error": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if serializer.is_valid():
            guest = serializer.save()
            tokens = self.get_tokens_for_guest(guest)
            return Response(tokens, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GuestDetailView(GenericAPIView):
    """
    Retrieve and update guest details view

    """

    serializer_class = GuestSerializer
    permission_classes = [IsAuthenticatedGuest]

    def get(self, request: Request) -> Response:
        """
        Retrieve guest details.

        Parameters
        ----------
        request : Request
            The request object.

        Returns
        -------
        Response
            The response object.
        """
        guest = request.user
        serializer = GuestSerializer(guest)

        return Response(serializer.data)

    def patch(self, request: Request) -> Response:
        """
        Update guest details.

        Parameters
        ----------
        request : Request
            The request object.

        Returns
        -------
        Response
            The response object.
        """

        guest = request.user
        serializer = GuestSerializer(guest, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GuestToUserView(GenericAPIView, AuthMixin):
    """
    Convert guest to user view.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedGuest]

    def post(self, request: Request) -> Response:
        """
        Post request to convert guest to user.

        Parameters
        ----------
        request : Request
            The request object.

        Returns
        -------
        Response
            The response object.
        """

        guest = request.user
        serializer = GuestSerializer(guest)

        try:
            guest = Guest.objects.get(guest_id=guest.guest_id)
        except Guest.DoesNotExist:
            return Response(
                {"error": "Guest not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user_data = {
            "username": guest.username,
            "email": request.data.get("email"),
            "password": request.data.get("password"),
        }

        serializer = self.get_serializer(data=user_data)

        if serializer.is_valid():
            user = serializer.save()

            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            tokens = self.get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayerViewSet(viewsets.ModelViewSet):
    """
    View for the Player model
    """

    serializer_class = PlayerSerializer
    http_method_names = ["get"]
    authentication_classes = []
    queryset = Player.objects.all()

    filter_backends = BACKENDS
    filterset_fields = [
        "player_id",
        "user",
        "guest",
        "wins",
        "losses",
        "draws",
        "total_games",
        "elo",
    ]
    search_fields = [
        "player_id",
        "user__username",
        "guest__username",
        "wins",
        "losses",
        "draws",
        "total_games",
        "elo",
    ]
    ordering_fields = filterset_fields

    def get_queryset(self):
        """
        Retrieve all players.

        """
        return (
            self.queryset.filter(is_human=True)
            .filter(Q(user__is_active=True) | Q(user__isnull=True))
            .order_by("player_id")
        )


class UpdateActivityView(GenericAPIView):
    """
    Update activity view
    """

    serializer_class = UpdateActivitySerializer

    def get_permissions(self):
        user = self.request.user
        if hasattr(user, "guest_id"):
            return [IsAuthenticatedGuest()]
        else:
            return [IsAuthenticated()]

    def post(self, request: Request) -> Response:
        """
        Post request to update activity

        Parameters
        ----------
        request : Request
            The request object.

        Returns
        -------
        Response
            The response object.

        """
        player = get_player(request.user)
        if not player:
            return Response(
                {"error": "Player does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        player.last_activity = timezone.now()
        player.save()
        return Response(
            {"message": "Activity updated"},
            status=status.HTTP_200_OK,
        )


class EloHistoryViewSet(viewsets.ModelViewSet):
    """
    View for the EloHistory model
    """

    serializer_class = EloHistorySerializer
    http_method_names = ["get"]
    authentication_classes = []
    queryset = EloHistory.objects.all()

    filter_backends = BACKENDS
    filterset_fields = [
        "elo_history_id",
        "player",
        "old_elo",
        "new_elo",
        "delta",
    ]
    search_fields = [
        "elo_history_id",
        "player__user__username",
        "player__user__user_id",
        "player__guest__username",
        "player__guest__guest_id",
        "player__algorithm__name",
        "player__algorithm__algorithm_id",
        "player__player_id",
        "old_elo",
        "new_elo",
        "delta",
        "created_at",
    ]
    ordering_fields = filterset_fields
