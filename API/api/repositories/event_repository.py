from api.models import Event
from datetime import date

class EventRepository:
    def create(self, name: str, event_date: date) -> Event:
        return Event.objects.create(name=name, event_date=event_date)