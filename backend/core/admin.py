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
    list_display = ["guest_id", "username"]


@admin.register(models.Algorithm)
class AlgorithmAdmin(admin.ModelAdmin):
    """
    Define the parameters to display on the admin page for Algorithm.

    """

    list_display = [
        "algorithm_id",
        "name",
        "code_name",
        "description",
        "depth",
    ]


@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
    """
    Define the parameters to display on the admin page for Player.

    """

    list_display = [
        "player_id",
        "user",
        "guest",
        "algorithm",
        "is_human",
        "wins",
        "losses",
        "draws",
        "total_games",
        "elo",
        "last_activity",
    ]

    list_filter = ["is_human"]


@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    """
    Define the parameters to display on the admin page for Status.

    """

    list_display = [
        "status_id",
        "name",
        "description",
    ]

    list_filter = ["status_id", "name", "description"]


@admin.register(models.Game)
class GameAdmin(admin.ModelAdmin):
    """
    Define the parameters to display on the admin page for Game.

    """

    list_display = [
        "game_id",
        "player_one",
        "player_two",
        "rows",
        "columns",
        "difficulty_level",
        "depth",
        "board",
        "status",
        "current_turn",
        "start_time",
        "end_time",
        "winner",
        "created_by",
        "created_at",
        "updated_at",
    ]

    list_filter = ["rows", "columns", "status", "difficulty_level", "depth"]


@admin.register(models.MatchMakingQueue)
class MatchMakingQueueAdmin(admin.ModelAdmin):
    """
    Define the parameters to display on the admin page for MatchMakingQueue.

    """

    list_display = [
        "queue_id",
        "player",
        "status",
        "game",
        "created_at",
        "updated_at",
    ]
    list_filter = ["status", "game"]


@admin.register(models.Move)
class MoveAdmin(admin.ModelAdmin):
    """
    Define the parameters to display on the admin page for Move.

    """

    list_display = [
        "move_id",
        "game",
        "player",
        "column",
        "row",
        "created_at",
    ]
    list_filter = ["column", "row"]


@admin.register(models.EloHistory)
class EloHistoryAdmin(admin.ModelAdmin):
    """
    Define the parameters to display on the admin page for EloHistory.

    """

    list_display = [
        "elo_history_id",
        "player",
        "old_elo",
        "new_elo",
        "delta",
        "created_at",
    ]
