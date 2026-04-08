from rest_framework.exceptions import ValidationError
from api.repositories.slot_repository import SlotRepository
from api.repositories.plage_repository import PlageRepository
from api.serializers.slot_serializer import SlotSerializer
from django.db import IntegrityError
from datetime import datetime
from django.utils.timezone import make_aware


class SlotService:
    def __init__(self):
        self.slot_repo = SlotRepository()
        self.plage_repo = PlageRepository()

    def book_slot(self, data: dict) -> dict:
        serializer = SlotSerializer(data=data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        vd = serializer.validated_data
        plage = vd["plage"]
        event = plage.event

        plage_start = make_aware(datetime.combine(event.event_date, plage.start_time))
        plage_end = make_aware(datetime.combine(event.event_date, plage.end_time))

        if vd["start_at"] < plage_start or vd["end_at"] > plage_end:
            raise ValidationError({
                "non_field_errors": (
                    "Le créneau doit être compris dans la plage "
                    f"({plage_start} – {plage_end})."
                )
            })

        try:
            slot = self.slot_repo.book(
                plage=vd["plage"], 
                start_at=vd["start_at"],
                end_at=vd["end_at"], 
                client_fname=vd["client_fname"], 
                client_lname=vd["client_lname"], 
                client_email=vd["client_email"], 
                client_phone=vd["client_phone"], 
                item=vd["item"], 
                item_description=vd["item_description"], 
                liability_accepted=vd["liability_accepted"]
            )
        except IntegrityError:
            raise ValidationError({"non_field_errors": "Cette plage horaire ne peut pas être réservée."})

        return SlotSerializer(slot).data