from api.models import Event, Plage, Slot
from django.db.models import Q
from datetime import date

class EventRepository:

    def get_event_by_id(self, event_id: int) -> Event | None:
        return Event.objects.filter(id=event_id).first()

    def has_booked_slots_for_event(self, event_id: int) -> bool:
        return Slot.objects.filter(
            plage__event_id=event_id,
            is_canceled=False,
        ).filter(
            (Q(client_fname__isnull=False) & ~Q(client_fname="")) |
            (Q(client_lname__isnull=False) & ~Q(client_lname="")) |
            (Q(client_email__isnull=False) & ~Q(client_email="")) |
            (Q(client_phone__isnull=False) & ~Q(client_phone=""))
        ).exists()

    def create(self, name: str, event_date: date) -> Event:
        return Event.objects.create(name=name, event_date=event_date)

    def update_event(self, event: Event) -> Event:
        event.save(update_fields=["name", "event_date"])
        return event