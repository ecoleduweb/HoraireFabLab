from rest_framework.exceptions import ValidationError
from api.repositories.event_repository import EventRepository
from api.serializers.event_serializer import EventSerializer
from django.db import IntegrityError


class EventService:
    def __init__(self):
        self.repo = EventRepository()

    def create_event(self, validated_data: dict) -> dict:
        try:
            event = self.repo.create(
                name=validated_data["name"],
                event_date=validated_data["event_date"],
            )
        except IntegrityError:
            raise ValidationError({"event_date": "Un événement existe déjà pour cette date."})

        return EventSerializer(event).data