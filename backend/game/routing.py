from django.urls import path


from . import consumers

websocket_urlpatterns = [
    path("<uuid:game_id>", consumers.GameConsumer.as_asgi()),
]
