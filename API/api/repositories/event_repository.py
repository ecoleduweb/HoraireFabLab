from api.models import Event
from datetime import date

class EventRepository:
    def create(self, event: Event) -> Event:
        event.save()
        return event