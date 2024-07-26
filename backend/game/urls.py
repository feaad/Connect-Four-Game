from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "game"

game_router = DefaultRouter(trailing_slash=False)
game_router.register("game", views.GameViewSet)

match_making_router = DefaultRouter(trailing_slash=False)
match_making_router.register(
    "match", views.GetMatchMakingQueueViewSet, basename="match"
)


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
    path("", include(game_router.urls)),
    path("match/", include(match_patterns)),
    path("", include(match_making_router.urls)),
]
