from datetime import date, datetime, time
from django.urls import reverse, NoReverseMatch
from api.models import Event, Plage, Slot
from api.tests.base_TestClass import BaseAPITestCase
from django.utils import timezone


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
        except NoReverseMatch:
            self.update_event_url = f"/api/events/{self.event.id}/update_date/"

    def test_update_event_date_requires_auth(self):
        resp = self.client.put(
            self.update_event_url,
            data={"name": "Repare tes trucks", "eventDate": "2026-05-20"},
            format="json",
        )
        self.assertIn(resp.status_code, (401, 403))

    def test_update_event_date_success_when_no_bookings(self):
        self.login_and_set_cookies()

        resp = self.client.put(
            self.update_event_url,
            data={"name": "Repare tes trucks v2", "eventDate": "2026-05-20"},
            format="json",
        )

        self.assertEqual(resp.status_code, 200)
        self.event.refresh_from_db()
        self.assertEqual(self.event.name, "Repare tes trucks v2")
        self.assertEqual(str(self.event.event_date), "2026-05-20")

    def test_update_event_date_fails_when_booked_slot_exists(self):
        self.login_and_set_cookies()

        Slot.objects.create(
            plage=self.plage,
            start_at=timezone.make_aware(datetime(2026, 5, 10, 9, 0)),
            end_at=timezone.make_aware(datetime(2026, 5, 10, 9, 30)),
            client_fname="Jean",
            client_email="jean@example.com",
            is_canceled=False,
        )

        resp = self.client.put(
            self.update_event_url,
            data={"name": "Repare tes trucks", "eventDate": "2026-05-20"},
            format="json",
        )

        self.assertEqual(resp.status_code, 400)
        self.assertIn("detail", resp.json())

        self.event.refresh_from_db()
        self.assertEqual(str(self.event.event_date), "2026-05-10")

    def test_update_event_date_missing_event_date_returns_400(self):
        self.login_and_set_cookies()

        resp = self.client.put(
            self.update_event_url,
            data={"name": "Repare tes trucks"},
            format="json",
        )

        self.assertEqual(resp.status_code, 400)
        self.assertIn("eventDate", resp.json())

    def test_update_event_date_missing_name_returns_400(self):
        self.login_and_set_cookies()

        resp = self.client.put(
            self.update_event_url,
            data={"eventDate": "2026-05-20"},
            format="json",
        )

        self.assertEqual(resp.status_code, 400)
        self.assertIn("name", resp.json())

    def test_update_event_date_invalid_event_date_returns_400(self):
        self.login_and_set_cookies()

        resp = self.client.put(
            self.update_event_url,
            data={"name": "Repare tes trucks", "eventDate": "20-05-2026"},
            format="json",
        )

        self.assertEqual(resp.status_code, 400)
        self.assertIn("eventDate", resp.json())

    def test_update_event_date_not_found_returns_404(self):
        self.login_and_set_cookies()

        try:
            url = reverse("update_event_date", kwargs={"event_id": 999999})
        except Exception:
            url = "/api/events/999999/update_date/"

        resp = self.client.put(
            url,
            data={"name": "Repare tes trucks", "eventDate": "2026-05-20"},
            format="json",
        )

        self.assertEqual(resp.status_code, 404)

    def test_get_events_success_returns_200(self):
        self.login_and_set_cookies()

        resp = self.client.get(
            reverse("get_events"),
            format="json",
        )

        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.json(), list)
        
    def test_update_event_date_in_past_returns_400(self):
        self.login_and_set_cookies()

        resp = self.client.put(
            self.update_event_url,
            data={"name": "Repare tes trucks", "eventDate": "2020-01-01"},
            format="json",
        )

        self.assertEqual(resp.status_code, 400)
        self.assertIn("detail", resp.json())

    def test_update_event_date_duplicate_returns_400(self):
        self.login_and_set_cookies()

        Event.objects.create(
            name="Autre événement",
            event_date=date(2026, 5, 20),
        )

        resp = self.client.put(
            self.update_event_url,
            data={"name": "Repare tes trucks", "eventDate": "2026-05-20"},
            format="json",
        )

        self.assertEqual(resp.status_code, 400)
        self.assertIn("eventDate", resp.json())


class CreateEventTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.create_event_url = reverse("create_event")

    def test_create_event_success_returns_201(self):
        self.login_and_set_cookies()
        resp = self.client.post(
            self.create_event_url,
            data={"name": "Journée portes ouvertes", "eventDate": "2026-05-15"},
            format="json",
        )
        self.assertEqual(resp.status_code, 201)

    def test_create_event_success_returns_correct_fields(self):
        self.login_and_set_cookies()
        resp = self.client.post(
            self.create_event_url,
            data={"name": "Journée portes ouvertes", "eventDate": "2026-05-15"},
            format="json",
        )
        body = resp.json()
        self.assertIn("id", body)
        self.assertIn("name", body)
        self.assertIn("eventDate", body)
        self.assertIn("createdAt", body)
        self.assertEqual(body["name"], "Journée portes ouvertes")
        self.assertEqual(body["eventDate"], "2026-05-15")

    def test_create_event_persists_in_db(self):
        self.login_and_set_cookies()
        self.client.post(
            self.create_event_url,
            data={"name": "Journée portes ouvertes", "eventDate": "2026-05-15"},
            format="json",
        )
        self.assertTrue(Event.objects.filter(event_date="2026-05-15").exists())

    # ── Authentification ─────────────────────────────────────

    def test_create_event_unauthenticated_returns_401(self):
        resp = self.client.post(
            self.create_event_url,
            data={"name": "Journée portes ouvertes", "eventDate": "2026-05-15"},
            format="json",
        )
        self.assertEqual(resp.status_code, 401)

    # ── Validation ───────────────────────────────────────────

    def test_create_event_missing_name_returns_400(self):
        self.login_and_set_cookies()
        resp = self.client.post(
            self.create_event_url,
            data={"eventDate": "2026-05-15"},
            format="json",
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("name", resp.json())

    def test_create_event_missing_date_returns_400(self):
        self.login_and_set_cookies()
        resp = self.client.post(
            self.create_event_url,
            data={"name": "Journée portes ouvertes"},
            format="json",
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("eventDate", resp.json())

    def test_create_event_invalid_date_format_returns_400(self):
        self.login_and_set_cookies()
        resp = self.client.post(
            self.create_event_url,
            data={"name": "Journée portes ouvertes", "eventDate": "15-05-2026"},
            format="json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_create_event_empty_name_returns_400(self):
        self.login_and_set_cookies()
        resp = self.client.post(
            self.create_event_url,
            data={"name": "", "eventDate": "2026-05-15"},
            format="json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_create_event_duplicate_date_returns_400(self):
        self.login_and_set_cookies()
        self.client.post(
            self.create_event_url,
            data={"name": "Premier événement", "eventDate": "2026-05-15"},
            format="json",
        )
        resp = self.client.post(
            self.create_event_url,
            data={"name": "Deuxième événement", "eventDate": "2026-05-15"},
            format="json",
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("eventDate", resp.json())
