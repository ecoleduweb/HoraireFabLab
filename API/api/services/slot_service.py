from rest_framework.exceptions import ValidationError
from api.repositories.slot_repository import SlotRepository
from api.repositories.plage_repository import PlageRepository
from api.repositories.event_repository import EventRepository
from api.serializers.slot_serializer import SlotSerializer
from django.db import IntegrityError
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from api.models import Slot


class SlotService:
    def __init__(self):
        self.slot_repo = SlotRepository()
        self.plage_repo = PlageRepository()
        self.event_repo = EventRepository()

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
    
    def get_available_slots(self, event_id) -> list[Slot]:
        current_event = self.event_repo.get_event_by_id(event_id)
        if current_event is None:
            raise ValidationError({"event_id": "Événement introuvable."})
        current_plages = self.plage_repo.get_active_plages_for_event(event_id)
        existing_slots = self.slot_repo.get_slots().filter(is_canceled=False)
        possible_slots = []


        for plage in current_plages:
            slot_duration = timedelta(minutes=plage.slot_duration_minutes)
            plage_start = make_aware(datetime.combine(current_event.event_date, plage.start_time))
            plage_end = make_aware(datetime.combine(current_event.event_date, plage.end_time))
            break_start = make_aware(datetime.combine(current_event.event_date, plage.break_start_time)) if plage.break_start_time else None
            break_end = make_aware(datetime.combine(current_event.event_date, plage.break_end_time)) if plage.break_end_time else None

            while plage_start + slot_duration <= plage_end:
                slot_end = plage_start + slot_duration

                if break_start and break_end and plage_start < break_end and slot_end > break_start:
                    plage_start = break_end
                    continue

                possible_slots.append(Slot(plage=plage, start_at=plage_start, end_at=slot_end))
                plage_start = slot_end

        existing_by_plage = {}
        for s in existing_slots:
            existing_by_plage.setdefault(s.plage_id, []).append((s.start_at, s.end_at))

        available_slots = []
        for candidate in possible_slots:
            overlaps = any(
                candidate.start_at < end_at and candidate.end_at > start_at
                for start_at, end_at in existing_by_plage.get(candidate.plage_id, [])
            )
            if not overlaps:
                available_slots.append(candidate)
            
        return available_slots
