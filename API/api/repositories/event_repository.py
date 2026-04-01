from api.models import Event

class EventRepository:
    def create(self, name: str, event_date) -> Event:
        return Event.objects.create(name=name, event_date=event_date)