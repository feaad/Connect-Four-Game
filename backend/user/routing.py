from django.urls import path


from . import consumers

websocket_urlpatterns = [
    path("<uuid:player_id>", consumers.PlayerConsumer.as_asgi()),
]
