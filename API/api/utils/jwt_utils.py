# api/utils/jwt_utils.py

from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings
from api.exceptions import TokenExpiredError, InvalidTokenError


class JwtUtils:

    @staticmethod
    def generate_tokens(username: str):
        """Génère des tokens JWT sans utiliser la base de données"""
        
        refresh = RefreshToken()
        refresh['username'] = username
        refresh['user_id'] = username
        
        access = refresh.access_token
        access['username'] = username
        
        return {
            "access": str(access),
            "refresh": str(refresh),
        }

    @staticmethod
    def decode_token(token: str):
        """Decode et vérifie un token JWT"""
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError()
        except jwt.InvalidTokenError:
            raise InvalidTokenError()