from datetime import date
from rest_framework.exceptions import NotFound, ValidationError, ConflictError
from api.serializers.event_serializer import EventSerializer
from django.db import IntegrityError
from api.repositories.event_repository import EventRepository


class EventService:
    def __init__(self):
        self.repo = EventRepository()

    def update_event(self, event_id: int, event_data: dict):

        event = self.repo.get_event_by_id(event_id)

        if not event:
            raise NotFound("Événement introuvable.")

        event_date = event_data["event_date"]

        if event_date < date.today():
            raise ValidationError({
                "detail": "La date de l'événement ne peut pas être dans le passé."
            })

        if self.repo.has_booked_slots_for_event(event.id):
            raise ConflictError({
                "detail": "Modification impossible: des inscriptions existent déjà."
            })

        event.name = event_data["name"]
        event.event_date = event_date

        try:
            return self.repo.update_event(event)
        except IntegrityError as err:
            raise ValidationError({
                "event_date": "Un événement existe déjà pour cette date."
            }) from err

    def create_event(self, data: dict) -> dict:
        serializer = EventSerializer(data=data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        try:
            event = self.repo.create(
                name=serializer.validated_data["name"],
                event_date=serializer.validated_data["event_date"],
            )
        except IntegrityError as err:
            raise ValidationError({"event_date": "Un événement existe déjà pour cette date."}) from err

        return EventSerializer(event).data


