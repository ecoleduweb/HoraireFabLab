# api/controllers/auth_controller.py

from django.conf import settings
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api.services.auth_service import AuthService

service = AuthService()

@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([]) 
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    result = service.login(username, password)  
    tokens = result["tokens"]

    response = Response({"username": result["username"]}, status=200)

    response.set_cookie(
        key="access_token",
        value=tokens["access"],
        httponly=True,
        secure=settings.JWT_COOKIE_SECURE,
        samesite="Lax",
        max_age=int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()),
        path="/",  # access dispo partout
    )

    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh"],
        httponly=True,
        secure=settings.JWT_COOKIE_SECURE,
        samesite="Lax",
        max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
        path="/",   # à corriger une fois le path crée
    )

    return response
