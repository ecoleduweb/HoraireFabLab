# api/exceptions/custom_exceptions.py

class ApiException(Exception):
    """Exception de base pour toutes les exceptions de l'API"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class InvalidCredentialsError(ApiException):
    """Erreur lorsque les identifiants sont invalides"""
    def __init__(self, message: str = "Identifiants invalides"):
        super().__init__(message, status_code=401)


class NotFoundError(ApiException):
    """Erreur lorsqu'une ressource n'est pas trouvée"""
    def __init__(self, message: str = "Ressource non trouvée"):
        super().__init__(message, status_code=404)


class BadRequestError(ApiException):
    """Erreur lorsque la requête est mal formée"""
    def __init__(self, message: str = "Requête invalide"):
        super().__init__(message, status_code=400)


class UnauthorizedError(ApiException):
    """Erreur lorsque l'utilisateur n'est pas autorisé"""
    def __init__(self, message: str = "Non autorisé"):
        super().__init__(message, status_code=403)


class ConflictError(ApiException):
    """Erreur lorsqu'il y a un conflit (ex: username déjà existant)"""
    def __init__(self, message: str = "Conflit détecté"):
        super().__init__(message, status_code=409)


class TokenExpiredError(ApiException):
    """Erreur lorsque le token JWT est expiré"""
    def __init__(self, message: str = "Token expiré"):
        super().__init__(message, status_code=401)


class InvalidTokenError(ApiException):
    """Erreur lorsque le token JWT est invalide"""
    def __init__(self, message: str = "Token invalide"):
        super().__init__(message, status_code=401)