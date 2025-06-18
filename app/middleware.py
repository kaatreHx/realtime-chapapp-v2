# yourapp/middleware.py

from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from asgiref.sync import sync_to_async
from app.models import CustomUser  # 🔁 Replace with your actual user model

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token", [None])[0]

        print("🔍 Raw token from query:", token)

        if token is None:
            scope["user"] = AnonymousUser()
            return await super().__call__(scope, receive, send)

        try:
            # Validate token
            UntypedToken(token)

            # Decode token
            decoded = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded.get("user_id")
            print("✅ Token decoded. User ID:", user_id)

            user = await self.get_user(user_id)
            scope["user"] = user
        except (InvalidToken, TokenError) as e:
            print("❌ Invalid token:", e)
            scope["user"] = AnonymousUser()
        except Exception as e:
            print("❌ General error in middleware:", e)
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    @sync_to_async
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return AnonymousUser()
