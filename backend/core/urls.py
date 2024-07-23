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
from user.views import LoginView, LogoutAllView, LogoutView

from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    HealthCheckView,
)

app_name = "core"

auth_patterns = (
    [
        path("login", LoginView.as_view(), name="login"),
        path("logout", LogoutView.as_view(), name="logout"),
        path("logout/all", LogoutAllView.as_view(), name="logout-all"),
    ],
    "auth",
)

token_patterns = (
    [
        path(
            "", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"
        ),
        path(
            "/refresh", CustomTokenRefreshView.as_view(), name="token_refresh"
        ),
        path(
            "/verify",
            CustomTokenVerifyView.as_view(),
            name="token_verify",
        ),
    ],
    "token",
)

urlpatterns = [
    path("health-check", HealthCheckView.as_view(), name="health-check"),
    path("auth/", include(auth_patterns)),
    path("token", include(token_patterns)),
]
