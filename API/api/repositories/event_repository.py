from api.models import Event, Plage, Slot
from django.db.models import Q
from datetime import date

class EventRepository:

    def get_event_by_id(self, event_id: int) -> Event | None:
        return Event.objects.filter(id=event_id).first()

    def get_plage_ids_by_event_id(self, event_id: int) -> list[int]:
        return list(
            Plage.objects.filter(event_id=event_id).values_list("id", flat=True)
        )

    def has_booked_slots(self, plage_ids: list[int]) -> bool:
        if not plage_ids:
            return False

        return Slot.objects.filter(
            plage_id__in=plage_ids,
            is_canceled=False,
        ).filter(
            (Q(client_fname__isnull=False) & ~Q(client_fname="")) |
            (Q(client_lname__isnull=False) & ~Q(client_lname="")) |
            (Q(client_email__isnull=False) & ~Q(client_email="")) |
            (Q(client_phone__isnull=False) & ~Q(client_phone=""))
        ).exists()

    def create(self, name: str, event_date: date) -> Event:
        return Event.objects.create(name=name, event_date=event_date)

    def update_event(self, event: Event, update_fields: list[str]) -> Event:
        event.save(update_fields=update_fields)
        return event