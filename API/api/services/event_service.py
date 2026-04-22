from datetime import date
from rest_framework.exceptions import NotFound, ValidationError, ConflictError
from api.serializers.event_serializer import EventSerializer
from django.db import IntegrityError
from api.repositories.event_repository import EventRepository




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

        if name is not None and not name.strip():
            raise ValidationError({"detail": "Le nom de l'événement ne peut pas être vide."})

        if name is None and event_date is None:
            raise ValidationError({"detail": "Au moins un champ à modifier est requis."})

        update_fields: list[str] = []

        if name is not None and name != event.name:
            event.name = name
            update_fields.append("name")

        if event_date is not None and event_date != event.event_date:
            plage_ids = self.repo.get_plage_ids_by_event_id(event.id)

            if self.repo.has_booked_slots(plage_ids):
                raise ConflictError({
                    "detail": "Modification impossible: des inscriptions existent déjà."
                })

            event.event_date = event_date
            update_fields.append("event_date")

        if not update_fields:
            return event

        try:
            return self.repo.update_event(event, update_fields=update_fields)
        except IntegrityError:
            raise ValidationError({"event_date": "Un événement existe déjà pour cette date."})

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
        

