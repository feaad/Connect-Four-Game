"""
File: admin.py
Project: Backend - Connect Four
File Created: Thursday, 18th July 2024 12:18:44 PM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: Admin Panel for the system.
-----
Last Modified: Thursday, 18th July 2024 6:02:25 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from core import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

admin.site.site_header = "Connect Four"
admin.site.index_title = "Connect Four Admin Panel"


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    """
    Define the parameters to display on the admin page for User.

    """

    ordering = ["user_id"]
    list_display = ["username"]

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password",
                    "email",
                    "profile_picture",
                    "is_auth_logs",
                    "is_adv_logs",
                ),
            },
        ),
    )
    list_display = [
        "user_id",
        "username",
        "password",
        "email",
        "profile_picture",
        "is_auth_logs",
        "is_adv_logs",
        "is_active",
        "is_staff",
        "is_superuser",
    ]


@admin.register(models.Guest)
class GuestAdmin(admin.ModelAdmin):
    """
    Define the parameters to display on the admin page for Guest.

    """

    ordering = ["guest_id"]
    readonly_fields = ["session_id"]
    list_display = ["guest_id", "session_id", "username"]
