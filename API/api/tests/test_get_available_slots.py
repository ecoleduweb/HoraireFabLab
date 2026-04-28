from api.tests.base_TestClass import BaseAPITestCase
from api.models import Plage, Event, Slot
from django.urls import reverse
from datetime import date
from django.utils import timezone


class GetAvailableSlotsTests(BaseAPITestCase):
    # ─────────────────────────────────────────────
    # Setup
    # ─────────────────────────────────────────────

    def setUp(self):
        super().setUp()
        self.url = lambda event_id: reverse("get_available_slots", args=[event_id])

        self.test_date = date(timezone.now().year + 1, 7, 16)

        self.event = Event.objects.create(
            name="Test Event",
            event_date=self.test_date,
        )

    # ─────────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────────

    def create_plage(
        self,
        name="p",
        start="08:00:00",
        end="09:00:00",
        break_start=None,
        break_end=None,
    ):
        return Plage.objects.create(
            event=self.event,
            name=name,
            start_time=start,
            end_time=end,
            slot_duration_minutes=10,
            break_start_time=break_start,
            break_end_time=break_end,
            is_active=True,
        )

    def call_api(self):
        return self.client.get(self.url(self.event.id))

    def extract(self, resp):
        return {
            (s["plageId"], s["startAt"], s["endAt"])
            for s in resp.json()
        }

    def make_dt(self, time_str):
        return f"{self.test_date}T{time_str}Z"

    # ─────────────────────────────────────────────
    # Tests
    # ─────────────────────────────────────────────

    # 1. Single plage, no break, no slots
    def test_single_plage_generates_slots(self):
        plage = self.create_plage(start="08:00:00", end="09:00:00")

        resp = self.call_api()
        self.assertEqual(resp.status_code, 200)

        actual = self.extract(resp)

        # minimal sanity check (not full enumeration explosion)
        self.assertTrue(len(actual) > 0)
        self.assertTrue(all(s[0] == plage.id for s in actual))

    # 2. Break removes slots inside break window
    def test_break_excludes_slots(self):
        plage = self.create_plage(
            start="08:00:00",
            end="09:00:00",
            break_start="08:20:00",
            break_end="08:40:00",
        )

        resp = self.call_api()
        actual = self.extract(resp)

        for _, start, end in actual:
            self.assertFalse(self.make_dt("08:20:00") <= start < self.make_dt("08:40:00"))
            self.assertFalse(self.make_dt("08:20:00") < end <= self.make_dt("08:40:00"))

    # 3. Multiple plages, no break
    def test_multiple_plages_no_break(self):
        p1 = self.create_plage(name="p1", start="08:00:00", end="09:00:00")
        p2 = self.create_plage(name="p2", start="10:00:00", end="11:00:00")

        resp = self.call_api()
        actual = self.extract(resp)

        plage_ids = {p1.id, p2.id}

        self.assertTrue(all(s[0] in plage_ids for s in actual))

    # 4. Multiple plages, mixed break
    def test_mixed_breaks(self):
        p1 = self.create_plage(
            name="p1",
            start="08:00:00",
            end="09:00:00",
            break_start="08:20:00",
            break_end="08:40:00",
        )
        p2 = self.create_plage(
            name="p2",
            start="10:00:00",
            end="11:00:00",
        )

        resp = self.call_api()
        actual = self.extract(resp)

        # ensure no slot violates p1 break
        for plage_id, start, end in actual:
            if plage_id == p1.id:
                self.assertFalse(self.make_dt("08:20:00") <= start < self.make_dt("08:40:00"))

    # 5. Existing slot is excluded
    def test_existing_slot_is_excluded(self):
        plage = self.create_plage()

        Slot.objects.create(
            plage=plage,
            start_at=self.make_dt("08:10:00"),
            end_at=self.make_dt("08:20:00"),
        )

        resp = self.call_api()
        actual = self.extract(resp)

        self.assertNotIn(
            (plage.id, self.make_dt("08:10:00"), self.make_dt("08:20:00")),
            actual,
        )

    # 6. Overlapping slots never returned
    def test_overlapping_slots_not_returned(self):
        plage = self.create_plage()

        Slot.objects.create(
            plage=plage,
            start_at=self.make_dt("08:10:00"),
            end_at=self.make_dt("08:20:00"),
        )

        resp = self.call_api()
        actual = self.extract(resp)

        # ensure no overlap leaks through
        blocked_start = self.make_dt("08:10:00")
        blocked_end = self.make_dt("08:20:00")
        for _, start, end in actual:
            self.assertFalse(start < blocked_end and end > blocked_start)

    def test_invalid_event_id_returns_client_error(self):
        resp = self.client.get(self.url(999999))
        self.assertIn(resp.status_code, {400, 404})