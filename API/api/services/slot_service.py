from rest_framework.exceptions import ValidationError
from api.repositories.slot_repository import SlotRepository
from api.serializers.slot_serializer import SlotSerializer
from django.db import IntegrityError
from datetime import datetime
from django.utils.timezone import make_aware
from api.models import Slot


class SlotService:
    def __init__(self):
        self.slot_repo = SlotRepository()

    def book_slot(self, slot: Slot) -> dict:
        plage = slot.plage
        event = plage.event

        # make_aware rend le datetime conscient de son fuseau horaire, ce qui permet de comparer les datetime
        # sur une base commune en s'assurant qu'elles sont dans le même fuseau horaire
        plage_start = make_aware(datetime.combine(event.event_date, plage.start_time))
        plage_end = make_aware(datetime.combine(event.event_date, plage.end_time))

        if slot.start_at < plage_start or slot.end_at > plage_end:
            raise ValidationError({
                "non_field_errors": (
                    "Le créneau doit être compris dans la plage "
                    f"({plage_start} - {plage_end})."
                )
            })

        overlapping_slots = self.slot_repo.find_overlapping(
            plage=plage,
            start_at=slot.start_at,
            end_at=slot.end_at
        )

        if overlapping_slots.exists():
            raise ValidationError({
                "non_field_errors": "Ce créneau est déjà réservé."
            })

        try:
            booked_slot = self.slot_repo.book(slot)
        except IntegrityError as e:
            raise ValidationError({"non_field_errors": "Cette plage horaire ne peut pas être réservée."}) from e

        return SlotSerializer(booked_slot).data