from datetime import datetime
from rest_framework.exceptions import NotFound, ValidationError,APIException
from api.serializers.event_serializer import EventSerializer
from django.db import IntegrityError
from api.repositories.event_repository import EventRepository

class ConflictError(APIException):
    status_code = 409
    default_detail = "Conflit détecté."
    default_code = "conflict"


class EventService:
    def __init__(self):
        self.repo = EventRepository()


    def update_event_date(self, event_id: int, event_date_raw: str):
        if not event_date_raw:
            raise ValidationError({"detail": "event_date est requis (YYYY-MM-DD)."})

        try:
            new_event_date = datetime.fromisoformat(event_date_raw).date()
        except ValueError as err:
            raise ValidationError({"detail": "event_date invalide (format attendu: YYYY-MM-DD)."}) from err

        event = self.repo.get_event_by_id(event_id)
        if not event:
            raise NotFound("Événement introuvable.")
        
        plage_ids = self.repo.get_plage_ids_by_event_id(event.id)
        if self.repo.has_booked_slots(plage_ids):
            raise ConflictError({
                "detail": "Modification impossible: des inscriptions existent déjà."
            })

        event.event_date = new_event_date
        event.save(update_fields=["event_date"])
        return event

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
    

