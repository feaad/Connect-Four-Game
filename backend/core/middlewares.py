# middlewares.py

import jwt
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken

from core.authentications import CustomJWTAuthentication


class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)
        self.authenticator = CustomJWTAuthentication()

    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])
        if b"authorization" in headers:
            try:
                token_name, token_key = (
                    headers[b"authorization"].decode().split()
                )
                if token_name == "Bearer":
                    validated_token = self.authenticator.get_validated_token(
                        token_key
                    )
                    user = await database_sync_to_async(
                        self.authenticator.get_user
                    )(validated_token)
                    scope["user"] = user
                else:
                    scope["user"] = AnonymousUser()
            except (jwt.exceptions.InvalidTokenError, InvalidToken):
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)
