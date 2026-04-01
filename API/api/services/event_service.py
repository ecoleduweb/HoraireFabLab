from rest_framework.exceptions import ValidationError
from api.repositories.event_repository import EventRepository
from api.serializers.event_serializer import EventSerializer


class EventService:
    def __init__(self):
        self.repo = EventRepository()

    def create_event(self, data: dict) -> dict:
        serializer = EventSerializer(data=data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        event_date = serializer.validated_data["event_date"]

        if self.repo.exists_by_date(event_date):
            raise ValidationError({"event_date": "Un événement existe déjà pour cette date."})

        event = self.repo.create(
            name=serializer.validated_data["name"],
            event_date=event_date,
        )

        return EventSerializer(event).data