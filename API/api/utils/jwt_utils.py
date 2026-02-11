# api/utils/jwt_utils.py

from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.exceptions import AuthenticationFailed


class JwtUtils:

    @staticmethod
    def generate_tokens(username: str, user_id: int | None = None):
        """Génère des tokens JWT sans utiliser la base de données"""

        refresh = RefreshToken()
        refresh["username"] = username

        if user_id is not None:
            refresh["user_id"] = user_id

        access = refresh.access_token  # hérite des claims du refresh

        return {
            "access": str(access),
            "refresh": str(refresh),
        }

    @staticmethod
    def decode_token(token: str):
        """
        Valide un token JWT via SimpleJWT et retourne le payload.
        DRF gère automatiquement les réponses 401.
        """
        try:
            validated_token = UntypedToken(token)
            return validated_token.payload

        except InvalidToken:
            raise AuthenticationFailed("Token invalide")

        except TokenError:
            raise AuthenticationFailed("Token expiré")
