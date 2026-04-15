# api/repositories/event_repository.py
from api.models import Event,Plage,Slot
from django.db.models import Q

class EventRepository:
    def get_event_by_id(self, event_id: int) -> Event | None:
        return Event.objects.filter(id=event_id).first()
    
    def get_plage_by_id(self, plage_id: int) -> Plage | None:
        return(
            Plage.objects.select_related('event').filter(id=plage_id).first()
        )
    
    def get_plages_by_event_id(self, event_id: int):
        return Plage.objects.filter(event_id=event_id).order_by('start_time')
    
    def has_booked_slots(self, plage_ids: list[int]) -> bool:
        if not plage_ids:
            return False

        return Slot.objects.filter(
            plage_id__in=plage_ids,
            is_canceled=False,
        ).filter(
            Q(client_fname__isnull=False) & ~Q(client_fname="") |
            Q(client_lname__isnull=False) & ~Q(client_lname="") |
            Q(client_email__isnull=False) & ~Q(client_email="") |
            Q(client_phone__isnull=False) & ~Q(client_phone="")
        ).exists()

