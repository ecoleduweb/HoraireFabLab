from api.models import Event

class EventRepository:
    def exists_by_date(self, event_date) -> bool:
        return Event.objects.filter(event_date=event_date).exists()

    def create(self, name: str, event_date) -> Event:
        return Event.objects.create(name=name, event_date=event_date)