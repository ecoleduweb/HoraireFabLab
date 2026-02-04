# api/controllers/auth_controller.py

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.services.auth_service import AuthService

service = AuthService()

@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    try:
        result = service.login(username, password)
        return JsonResponse(result)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=401)
