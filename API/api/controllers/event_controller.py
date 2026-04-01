from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from api.services.event_service import EventService

service = EventService()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_event(request):
    try:
        event = service.create_event(request.data)
        return Response(event, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)