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

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from user.views import LoginView, LogoutView

from .views import HealthCheckView

app_name = "core"

urlpatterns = [
    path("health-check", HealthCheckView.as_view(), name="health-check"),
    path("auth/login", LoginView.as_view(), name="login"),
    path("auth/logout", LogoutView.as_view(), name="logout"),
    path("token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify", TokenVerifyView.as_view(), name="token_verify"),
]
