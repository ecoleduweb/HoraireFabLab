# api/services/auth_service.py

from api.repositories.auth_repository import AuthRepository
from api.utils.jwt_utils import JwtUtils
from api.exceptions import InvalidCredentialsError, BadRequestError


class AuthService:
    def __init__(self):
        self.repo = AuthRepository()

    def login(self, username, password):
        # Validation
        if not username or not password:
            raise BadRequestError("Username et password sont requis")
        
        # Authentification
        user = self.repo.find_user(username, password)

        if not user:
            raise InvalidCredentialsError("Username ou password incorrect")

        # Génération des tokens
        tokens = JwtUtils.generate_tokens(username)

        return {
            "message": "Login successful",
            "username": username,
            "tokens": tokens
        }