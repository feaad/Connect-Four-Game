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

from django.urls import path

from . import views

app_name = "user"

urlpatterns = [
    path("/register", views.RegisterView.as_view(), name="user-register"),
    path("", views.UserDetailView.as_view(), name="user-detail"),
]
