# middlewares.py

import jwt
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from core.authentications import CustomJWTAuthentication
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken


class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)
        self.authenticator = CustomJWTAuthentication()

    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])
        query_string = scope["query_string"]
        token = None

        # check if token is in query string
        if query_string and b"token=" in query_string:
            token = query_string.decode().split("token=")[1]

        elif b"authorization" in headers:
            token_name, token_key = headers[b"authorization"].decode().split()
            if token_name == "Bearer":
                token = token_key

        if token:
            try:
                validated_token = self.authenticator.get_validated_token(token)
                user = await database_sync_to_async(
                    self.authenticator.get_user
                )(validated_token)
                scope["user"] = user

            except (jwt.exceptions.InvalidTokenError, InvalidToken):
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)
