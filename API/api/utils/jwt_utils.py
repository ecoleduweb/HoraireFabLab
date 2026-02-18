# api/utils/jwt_utils.py

from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.exceptions import AuthenticationFailed


class JwtUtils:

    @staticmethod
    def generate_tokens(username: str, user_id: int):
        refresh = RefreshToken()
        refresh["username"] = username
        refresh["user_id"] = user_id

        access = refresh.access_token

        return {"access": str(access), "refresh": str(refresh)}

    @staticmethod
    def decode_token(token: str):
        try:
            validated = UntypedToken(token)
            return validated.payload
        except (InvalidToken, TokenError):
            raise AuthenticationFailed("Token invalide ou expiré")
