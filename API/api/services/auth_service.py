# api/services/auth_service.py

from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from api.repositories.auth_repository import AuthRepository
from api.utils.jwt_utils import JwtUtils


class AuthService:
    def __init__(self):
        self.repo = AuthRepository()

    def login(self, username: str | None, password: str | None):
        if not username or not password:
            raise ValidationError({"detail": "Username et password sont requis"})

        user = self.repo.get_user_by_username(username)
        if not user:
            raise AuthenticationFailed("Username ou password incorrect")

        if not check_password(password, user.password_hash):
            raise AuthenticationFailed("Username ou password incorrect")

        tokens = JwtUtils.generate_tokens(username=user.username, user_id=user.id)

        return {
            "username": user.username,
            "tokens": tokens,
        }
