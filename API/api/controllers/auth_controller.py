# api/controllers/auth_controller.py
from django.conf import settings
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
    except AuthenticationFailed as e:
        return Response({"detail": str(e)}, status=401)
    except ValidationError as e:
        return Response(e.detail, status=400)

    tokens = result["tokens"]
    response = Response({"username": result["username"]}, status=200)

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
