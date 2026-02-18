# api/repositories/auth_repository.py

from api.models import User  

class AuthRepository:
    def get_user_by_username(self, username: str) -> User | None:
        return User.objects.filter(username=username).first()
