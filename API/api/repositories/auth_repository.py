# api/repositories/auth_repository.py

class Auth_Repository:
    def __init__(self):
        # Hardcoded admins
        self.admins = [
            {"username": "admin1", "password": "pass123"},
            {"username": "admin2", "password": "pass456"},
        ]

    def find_admin(self, username, password):
        for admin in self.admins:
            if admin["username"] == username and admin["password"] == password:
                return admin
        return None
