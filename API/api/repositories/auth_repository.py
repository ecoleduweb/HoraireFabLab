# api/repositories/auth_repository.py

class AuthRepository:
    def __init__(self):
        # Hardcoded admins
        self.admins = [
            {"username": "admin1", "password": "pass123"},
            {"username": "admin2", "password": "pass456"},
        ]

    def find_user(self, username, password):
        for user in self.admins:
            if user["username"] == username and user["password"] == password:
                return user
        return None