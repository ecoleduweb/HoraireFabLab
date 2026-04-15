from api.models import Slot

class SlotRepository:
    def get_slots(self):
        return Slot.objects.all()
    
    def find_overlapping(self, plage, start_at, end_at):
        return self.get_slots().filter(
            plage=plage,
            is_canceled=False
        ).filter(
            start_at__lt=end_at,
            end_at__gt=start_at
        )

    def book(self, slot: Slot) -> Slot:
        slot.save()
        return slot