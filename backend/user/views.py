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


from core.models import Guest, Player, User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from user.permissions import GuestHasSessionID
from user.serializers import GuestSerializer, PlayerSerializer, UserSerializer

from .mixins import AuthMixin

backends = [
    DjangoFilterBackend,
    filters.SearchFilter,
    filters.OrderingFilter,
]


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


class GuestViewSet(viewsets.ModelViewSet):
    """
    View for the Guest model
    """

    serializer_class = GuestSerializer
    permission_classes = [GuestHasSessionID]
    authentication_classes = []
    queryset = Guest.objects.all()

    def perform_create(self, serializer):
        username = self.request.data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError({"error": "Username already exists"})

        serializer.save()

        response = Response(serializer.data, status=status.HTTP_201_CREATED)
        response.set_cookie(
            "guest_id",
            serializer.data["guest_id"],
            httponly=True,  # HttpOnly flag for security
            secure=True,
            samesite="Strict",
        )
        return response


class GuestToUserView(GenericAPIView, AuthMixin):
    """
    Convert guest to user view.
    """

    serializer_class = UserSerializer
    permission_classes = [GuestHasSessionID]
    authentication_classes = []

    def post(self, request: Request, guest_id: str) -> Response:
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

        try:
            guest = Guest.objects.get(guest_id=guest_id)
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
            tokens = self.get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayerViewSet(viewsets.ModelViewSet):
    """
    View for the Guest model
    """

    serializer_class = PlayerSerializer
    http_method_names = ["get"]
    authentication_classes = []
    queryset = Player.objects.all()

    filter_backends = backends
    filterset_fields = ["player_id", "user", "guest"]
    search_fields = ["player_id", "user__username", "guest__username"]
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
