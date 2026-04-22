from rest_framework.exceptions import ValidationError
from api.repositories.event_repository import EventRepository
from api.serializers.event_serializer import EventSerializer
from django.db import IntegrityError


class EventService:
    def __init__(self):
        self.repo = EventRepository()

    def create_event(self, data: dict) -> dict:
        serializer = EventSerializer(data=data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        try:
            event = self.repo.create(
                name=serializer.validated_data["name"],
                event_date=serializer.validated_data["event_date"],
            )
        except IntegrityError:
            raise ValidationError({"event_date": "Un événement existe déjà pour cette date."})

        return EventSerializer(event).data
    