"""
File: urls.py
Project: Backend - Connect Four
File Created: Friday, 19th July 2024 12:31:13 PM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: The URL configuration for the user app.
-----
Last Modified: Saturday, 20th July 2024 4:37:44 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from core.router import CustomRouter
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "user"


guest_router = CustomRouter(trailing_slash=False)
guest_router.register("guest", views.GuestViewSet)

player_router = DefaultRouter(trailing_slash=False)
player_router.register("player", views.PlayerViewSet)

user_patterns = (
    [
        path("/register", views.RegisterView.as_view(), name="user-register"),
        path("", views.UserDetailView.as_view(), name="user-detail"),
    ],
    "user",
)

urlpatterns = [
    path("user", include(user_patterns)),
    path(
        "guest/<str:guest_id>/register",
        views.GuestToUserView.as_view(),
        name="guest-register",
    ),
    path("", include(guest_router.urls)),
    path("", include(player_router.urls)),
]
