from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from api.services.event_service import EventService
from api.serializers.event_serializer import EventSerializer
from datetime import date


service = EventService()

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_event_date(request, event_id: int):

    event_date_raw = request.data.get("event_date")
    name = request.data.get("name")  # Optionnel, peut être utilisé pour mettre à jour le nom en même temps
    event_date = None

    if not event_date_raw:
        raise ValidationError({"detail": "event_date est requis (YYYY-MM-DD)."})

    try:
        event_date = date.fromisoformat(event_date_raw)
    except ValueError:
        raise ValidationError({"detail": "event_date invalide (format attendu: YYYY-MM-DD)."})

    event = service.update_event(
        event_id=event_id,
        name=name,
        event_date=event_date,
    )

    return Response(
        EventSerializer(event).data,
        status=status.HTTP_200_OK
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_event(request):
    try:
        event = service.create_event(request.data)
        return Response(event, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

