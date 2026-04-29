from api.models import Event, Plage, Slot
from django.db.models import Q
from datetime import date

class EventRepository:


    def has_booked_slots_for_event(self, event_id: int) -> bool:
        return Slot.objects.filter(
            plage__event_id=event_id,
            is_canceled=False,
        ).exists()

    def update_event(self, event: Event) -> Event:
        event.save(update_fields=["name", "event_date"])
        return event

    def create(self, event: Event) -> Event:
        event.save()
        return event

    
    def get_event_by_id(self, event_id):
        try:
            return Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return None
    
    def get_all_events(self)-> list[Event]:
        return list(Event.objects.all().order_by("event_date"))

