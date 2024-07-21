"""
File: urls.py
Project: Backend - Connect Four
File Created: Wednesday, 17th July 2024 2:56:56 PM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: The URL configuration for the system.
-----
Last Modified: Thursday, 18th July 2024 6:08:00 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin", admin.site.urls),
    path("api/schema", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/swagger",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs-swagger",
    ),
    path(
        "api/docs/redoc",
        SpectacularRedocView.as_view(url_name="api-schema"),
        name="api-docs-redoc",
    ),
    path("api/", include("user.urls")),
    path("api/", include("core.urls")),
    path("api/", include("algorithm.urls")),
]
