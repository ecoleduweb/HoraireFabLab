# api/services/auth_service.py

from api.repositories.auth_repository import Auth_Repository

class AuthService:
    def __init__(self):
        self.repo = Auth_Repository()

    def login(self, username, password):
        admin = self.repo.find_admin(username, password)
        if not admin:
            raise ValueError("Invalid credentials")

        return {
            "message": "Login successful",
            "username": admin["username"]
        }
