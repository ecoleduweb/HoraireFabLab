# API/api/controllers/event_controller.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.services.event_service import EventService


service = EventService()

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_event_date(request, event_id: int):
    event = service.update_event_date(
        event_id=event_id,
        event_date_raw=request.data.get("event_date"),
    )

    return Response(
        {
            "id": event.id,
            "name": event.name,
            "event_date": str(event.event_date),
        },
        status=status.HTTP_200_OK,
    )