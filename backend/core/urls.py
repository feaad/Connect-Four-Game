"""
File: urls.py
Project: Backend - Connect Four
File Created: Saturday, 20th July 2024 4:23:28 PM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: The URL configuration for the core app.
-----
Last Modified: Saturday, 20th July 2024 4:37:06 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from user.views import LoginView, LogoutView

from .views import HealthCheckView

app_name = "core"

auth_patterns = (
    [
        path("login", LoginView.as_view(), name="login"),
        path("logout", LogoutView.as_view(), name="logout"),
    ],
    "auth",
)

token_patterns = (
    [
        path("", TokenObtainPairView.as_view(), name="token_obtain_pair"),
        path("refresh", TokenRefreshView.as_view(), name="token_refresh"),
        path("verify", TokenVerifyView.as_view(), name="token_verify"),
    ],
    "token",
)

urlpatterns = [
    path("health-check", HealthCheckView.as_view(), name="health-check"),
    path("auth/", include(auth_patterns)),
    path("token/", include(token_patterns)),
]