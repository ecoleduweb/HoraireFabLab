from api.models import Event
from datetime import date

class EventRepository:
  
    def create(self, event: Event) -> Event:
        event.save()
        return event
    
    def get_event_by_id(self, event_id):
        try:
            return Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return None

