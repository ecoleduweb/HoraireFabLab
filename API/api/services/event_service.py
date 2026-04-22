from datetime import date
from rest_framework.exceptions import NotFound, ValidationError, ConflictError
from api.serializers.event_serializer import EventSerializer
from django.db import IntegrityError
from api.repositories.event_repository import EventRepository
from datetime import date




class EventService:
    def __init__(self):
        self.repo = EventRepository()


    def update_event(self, event_id: int, name: str | None, event_date: date | None):

        event = self.repo.get_event_by_id(event_id)

        if not event:
            raise NotFound("Événement introuvable.")

        if event_date and event_date < date.today():
            raise ValidationError({
                "detail": "La date de l'événement ne peut pas être dans le passé."
            })

        plage_ids = self.repo.get_plage_ids_by_event_id(event.id)

        if self.repo.has_booked_slots(plage_ids):
            raise ConflictError({
                "detail": "Modification impossible: des inscriptions existent déjà."
            })

        if name is not None:
            event.name = name

        if event_date is not None:
            event.event_date = event_date

        return self.repo.update_event(event)

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
        

