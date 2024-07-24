from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "game"

game_router = DefaultRouter(trailing_slash=False)
game_router.register("game", views.GameViewSet)

game_patterns = (
    [
        path("/history", views.GameHistoryView.as_view(), name="game-history"),
        path("/create", views.CreateGameView.as_view(), name="game-create"),
    ],
    "game",
)

urlpatterns = [
    path("game", include(game_patterns)),
    path("", include(game_router.urls)),
]
