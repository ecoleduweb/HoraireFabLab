# api/auth/cookie_jwt_auth.py

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from types import SimpleNamespace


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get("access_token")
        if not raw_token:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except (InvalidToken, TokenError):
            raise AuthenticationFailed("Token invalide ou expiré")

        user_id = validated_token.get("user_id")
        if not user_id:
            raise AuthenticationFailed("Token invalide (user_id manquant)")

        # user issu du token
        user = SimpleNamespace(
            id=user_id,
        )

        return (user, validated_token)
