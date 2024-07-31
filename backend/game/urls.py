from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "game"

router = DefaultRouter(trailing_slash=False)
router.register("game", views.GameViewSet)
router.register(
    "match",
    views.GetMatchMakingQueueViewSet,
    basename="match",
)
router.register(
    "invitation", views.GameInvitationViewSet, basename="invitation"
)
router.register("move", views.MoveViewSet, basename="move")


game_patterns = (
    [
        path("/history", views.GameHistoryView.as_view(), name="game-history"),
        path("/create", views.CreateGameView.as_view(), name="game-create"),
    ],
    "game",
)

match_patterns = (
    [
        path(
            "request",
            views.RequestMatchMakingView.as_view(),
            name="match-request",
        ),
        path(
            "cancel",
            views.CancelMatchMakingView.as_view(),
            name="match-cancel",
        ),
    ],
    "match",
)

urlpatterns = [
    path("game", include(game_patterns)),
    path("match/", include(match_patterns)),
    path("", include(router.urls)),
    path(
        "api/move/<int:game_id>/undo",
        views.MoveViewSet.as_view({"post": "undo"}),
        name="move-undo",
    ),
]
