from channels.routing import URLRouter
from django.urls import path
from game import routing as game_routing
from user import routing as player_routing

websocket_urlpatterns = [
    path("ws/game/", URLRouter(game_routing.websocket_urlpatterns)),
    path("ws/player/", URLRouter(player_routing.websocket_urlpatterns)),
]
