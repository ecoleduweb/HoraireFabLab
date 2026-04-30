from asyncio import events

from rest_framework.exceptions import ValidationError
from api.repositories.event_repository import EventRepository
from datetime import date
from api.serializers.event_serializer import EventSerializer
from django.db import IntegrityError
from api.repositories.event_repository import EventRepository
from api.models import Event



class EventService:
    def __init__(self):
        self.repo = EventRepository()

    def get_event_by_id(self, event_id: int) -> Event | None:
     return self.repo.get_event_by_id(event_id)

    def get_all_events(self)-> list:
        events= self.repo.get_all_events()
        return EventSerializer(events, many=True).data
    def create_event(self, event: Event) -> dict:
        try:
            event = self.repo.create(event)
        except IntegrityError:
            raise ValidationError({"event_date": "Un évènement existe déjà pour cette date."})

        return EventSerializer(event).data
    
    def get_upcoming_events(self) -> list:
        events = self.repo.get_upcoming_events()
        return EventSerializer(events, many=True).data
      
    def update_event(self,event: Event)-> dict:

        if event.event_date< date.today():
            raise ValidationError({
                "detail": "La date de l'évènement ne peut pas être dans le passé."
            })

        if self.repo.has_booked_slots_for_event(event.id):
            raise ValidationError({
                "detail": "Modification impossible: des inscriptions existent déjà."
            })

        try:
            event = self.repo.update_event(event)
        except IntegrityError as err:
            raise ValidationError({
                "event_date": "Un évènement existe déjà pour cette date."
            }) from err
        return EventSerializer(event).data
    

    
        
