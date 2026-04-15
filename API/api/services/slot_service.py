from rest_framework.exceptions import ValidationError
from api.repositories.slot_repository import SlotRepository
from api.serializers.slot_serializer import SlotSerializer
from django.db import IntegrityError
from datetime import datetime
from django.utils.timezone import make_aware
from zoneinfo import ZoneInfo
from api.models import Slot


class SlotService:
    def __init__(self):
        self.slot_repo = SlotRepository()

    def book_slot(self, data: dict) -> dict:
        
        plage = data["plage"]
        event = plage.event

        plage_start = make_aware(datetime.combine(event.event_date, plage.start_time))
        plage_end = make_aware(datetime.combine(event.event_date, plage.end_time))

        if data["start_at"] < plage_start or data["end_at"] > plage_end:
            raise ValidationError({
                "non_field_errors": (
                    "Le créneau doit être compris dans la plage "
                    f"({plage_start} - {plage_end})."
                )
            })
        
        overlapping_slots = self.slot_repo.find_overlapping(
            plage=plage,
            start_at=data["start_at"],
            end_at=data["end_at"]
        )

        if overlapping_slots.exists():
            raise ValidationError({
                "non_field_errors": ("Ce créneau est déjà réservé.")
            })

        try:
            slot = self.slot_repo.book(Slot(
                plage=data["plage"], 
                start_at=data["start_at"],
                end_at=data["end_at"], 
                client_fname=data["client_fname"], 
                client_lname=data["client_lname"], 
                client_email=data["client_email"], 
                client_phone=data["client_phone"], 
                item=data["item"], 
                item_description=data["item_description"], 
                liability_accepted=data["liability_accepted"])
            )
        except IntegrityError as e:
          raise ValidationError({"non_field_errors": "Cette plage horaire ne peut pas être réservée."}) from e

        return SlotSerializer(slot).data