# api/controllers/user_controller.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response({
        "username": request.auth.get("username")
    })