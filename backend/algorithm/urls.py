"""
File: urls.py
Project: Backend - Connect Four
File Created: Sunday, 21st July 2024 6:55:10 PM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: The URL configuration for the algorithm app.
-----
Last Modified: Sunday, 21st July 2024 7:31:31 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from algorithm import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = "algorithm"

router = DefaultRouter(trailing_slash=False)
router.register("algorithm", views.AlgorithmViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
