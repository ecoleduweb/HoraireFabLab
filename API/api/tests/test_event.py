from api.tests.base_TestClass import BaseAPITestCase
from api.models import Event
from django.urls import reverse
from datetime import date, timedelta


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

    def test_get_upcoming_events_excludes_past_includes_today_and_future(self):
        self.login_and_set_cookies()
        today = date.today()

        self.client.post(self.create_event_url, data={"name": "Passé", "eventDate": (today - timedelta(days=1)).isoformat()}, format="json")
        self.client.post(self.create_event_url, data={"name": "Aujourd'hui", "eventDate": today.isoformat()}, format="json")
        self.client.post(self.create_event_url, data={"name": "Futur", "eventDate": (today + timedelta(days=1)).isoformat()}, format="json")

        resp = self.client.get(reverse("get_upcoming_events"))
        self.assertEqual(resp.status_code, 200)

        body = resp.json()
        dates = [e["eventDate"] for e in body]
        self.assertNotIn((today - timedelta(days=1)).isoformat(), dates)
        self.assertIn(today.isoformat(), dates)
        self.assertIn((today + timedelta(days=1)).isoformat(), dates)