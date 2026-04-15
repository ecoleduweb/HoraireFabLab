from datetime import datetime
from rest_framework.exceptions import NotFound, ValidationError,APIException

from api.repositories.event_repository import EventRepository

class ConflictError(APIException):
    status_code = 409
    default_code = "conflict"

class EventService:
    def __init__(self):
        self.repo = EventRepository()

    def update_event_date(self, event_id: int, event_date_raw: str):
        if not event_date_raw:
            raise ValidationError({"detail": "event_date est requis (YYYY-MM-DD)."})

        try:
            new_event_date = datetime.fromisoformat(event_date_raw).date()
        except ValueError:
            raise ValidationError({"detail": "event_date invalide (format attendu: YYYY-MM-DD)."})

        event = self.repo.get_event_by_id(event_id)
        if not event:
            raise NotFound("Événement introuvable.")

        plage_ids = [p.id for p in self.repo.get_plages_by_event_id(event.id)]
        if self.repo.has_booked_slots(plage_ids):
            raise ConflictError({
                "detail": "Modification impossible: des inscriptions existent déjà."
            })

        event.event_date = new_event_date
        event.save(update_fields=["event_date"])
        return event