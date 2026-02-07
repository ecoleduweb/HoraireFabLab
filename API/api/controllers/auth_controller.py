# api/controllers/auth_controller.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api.services.auth_service import AuthService
from api.exceptions import ApiException

service = AuthService()

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    try:
        result = service.login(username, password)
        return Response(result, status=200)
    
    except ApiException as e:
        return Response(
            {"error": e.message},
            status=e.status_code
        )
    
    except Exception as e:
        return Response(
            {"error": "Erreur interne du serveur"},
            status=500
        )