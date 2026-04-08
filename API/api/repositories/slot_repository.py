from api.models import Slot
from datetime import date

class SlotRepository:
    def book(self, plage: int, start_at: date, end_at: date, client_fname: str, client_lname: str, client_email: str, client_phone: str, item: str, item_description: str, liability_accepted: bool) -> Slot:
        return Slot.objects.create(plage=plage, start_at=start_at, end_at=end_at, client_fname=client_fname, client_lname=client_lname, client_email=client_email, client_phone=client_phone, item=item, item_description=item_description, liability_accepted=liability_accepted)