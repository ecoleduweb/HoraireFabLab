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
        
    def get_upcoming_events(self):
        return Event.objects.filter(event_date__gte=date.today()).order_by('event_date')

