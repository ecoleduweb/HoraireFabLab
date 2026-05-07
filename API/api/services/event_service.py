from rest_framework.exceptions import ValidationError
from api.repositories.event_repository import EventRepository
from datetime import date
from django.db import IntegrityError
from api.repositories.event_repository import EventRepository
from api.models import Event



class EventService:
    def __init__(self):
        self.repo = EventRepository()

    def get_event_by_id(self, event_id: int) -> Event | None:
     return self.repo.get_event_by_id(event_id)

    def get_all_events(self)-> list[Event]:
        return self.repo.get_all_events()
       
    def create_event(self, event: Event) -> Event:
        try:
           return self.repo.create(event)
        except IntegrityError:
            raise ValidationError({"event_date": "Un évènement existe déjà pour cette date."})

    
    def get_upcoming_events(self) -> list[Event]:
        return self.repo.get_upcoming_events()
       
      
    def update_event(self,event: Event)-> Event:

        if event.event_date< date.today():
            raise ValidationError({
                "detail": "La date de l'évènement ne peut pas être dans le passé."
            })

        if self.repo.has_booked_slots_for_event(event.id):
            raise ValidationError({
                "detail": "Modification impossible: des inscriptions existent déjà."
            })

        try:
            return self.repo.update_event(event)
        except IntegrityError as err:
            raise ValidationError({
                "event_date": "Un évènement existe déjà pour cette date."
            }) from err
     
    

    
        
