# api/controllers/auth_controller.py
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from api.services.auth_service import AuthService

service = AuthService()

@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])  # Ignore l'authentification sur cette route.
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    try:
        result = service.login(username, password)
    except AuthenticationFailed:
        return Response({"detail": "Utilisateur ou mot de passe invalide"}, status=status.HTTP_401_UNAUTHORIZED)
    except ValidationError:
        return Response({"detail": "Utilisateur ou mot de passe invalide"}, status=status.HTTP_400_BAD_REQUEST)

    tokens = result["tokens"]
    response = Response({"username": result["username"]}, status=status.HTTP_200_OK)

    response.set_cookie(
        key="access_token",
        value=tokens["access"],
        httponly=True,
        secure=getattr(settings, "JWT_COOKIE_SECURE", not settings.DEBUG),
        samesite=getattr(settings, "JWT_COOKIE_SAMESITE", "Lax"),
        max_age=int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()),
        path="/",
    )

    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh"],
        httponly=True,
        secure=getattr(settings, "JWT_COOKIE_SECURE", not settings.DEBUG),
        samesite=getattr(settings, "JWT_COOKIE_SAMESITE", "Lax"),
        max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
        path="/",     # Ajuste le path selon ta vraie route refresh

    )
    return response

@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([]) # logout doit fonctionner même si token expiré
def logout(request):
    response = Response({"detail": "Déconnecté"}, status=status.HTTP_200_OK)
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")

    return response
