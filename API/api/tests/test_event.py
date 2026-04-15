from datetime import date, datetime, time

from django.urls import reverse

from api.models import Event, Plage, Slot
from api.tests.base_TestClass import BaseAPITestCase


class UpdateEventDateTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()

        self.event = Event.objects.create(
            name="Repare tes trucks",
            event_date=date(2026, 5, 10),
        )

        self.plage = Plage.objects.create(
            event=self.event,
            name="Matin",
            start_time=time(9, 0),
            end_time=time(12, 0),
            slot_duration_minutes=30,
        )

        try:
            self.update_event_url = reverse(
                "update_event_date", kwargs={"event_id": self.event.id}
            )
        except Exception:
            self.update_event_url = f"/api/events/{self.event.id}/update_date/"

    def test_update_event_date_requires_auth(self):
        resp = self.client.put(
            self.update_event_url,
            data={"event_date": "2026-05-20"},
            format="json",
        )
        self.assertIn(resp.status_code, (401, 403))

    def test_update_event_date_success_when_no_bookings(self):
        self.login_and_set_cookies()

        resp = self.client.put(
            self.update_event_url,
            data={"event_date": "2026-05-20"},
            format="json",
        )

        self.assertEqual(resp.status_code, 200)
        self.event.refresh_from_db()
        self.assertEqual(str(self.event.event_date), "2026-05-20")

    def test_update_event_date_fails_when_booked_slot_exists(self):
        self.login_and_set_cookies()

        Slot.objects.create(
            plage=self.plage,
            start_at=datetime(2026, 5, 10, 9, 0),
            end_at=datetime(2026, 5, 10, 9, 30),
            client_fname="Jean",
            client_email="jean@example.com",
            is_canceled=False,
        )

        resp = self.client.put(
            self.update_event_url,
            data={"event_date": "2026-05-20"},
            format="json",
        )

        self.assertEqual(resp.status_code, 409)
        self.assertIn("detail", resp.json())

        self.event.refresh_from_db()
        self.assertEqual(str(self.event.event_date), "2026-05-10")

    def test_update_event_date_missing_event_date_returns_400(self):
        self.login_and_set_cookies()

        resp = self.client.put(
            self.update_event_url,
            data={},
            format="json",
        )

        self.assertEqual(resp.status_code, 400)
        self.assertIn("detail", resp.json())

    def test_update_event_date_invalid_event_date_returns_400(self):
        self.login_and_set_cookies()

        resp = self.client.put(
            self.update_event_url,
            data={"event_date": "20-05-2026"},
            format="json",
        )

        self.assertEqual(resp.status_code, 400)
        self.assertIn("detail", resp.json())

    def test_update_event_date_not_found_returns_404(self):
        self.login_and_set_cookies()

        try:
            url = reverse("update_event_date", kwargs={"event_id": 999999})
        except Exception:
            url = "/api/events/999999/update_date/"

        resp = self.client.put(
            url,
            data={"event_date": "2026-05-20"},
            format="json",
        )

        self.assertEqual(resp.status_code, 404)