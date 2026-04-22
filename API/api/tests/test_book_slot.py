from api.tests.base_TestClass import BaseAPITestCase
from api.models import Slot, Plage, Event
from django.urls import reverse
from datetime import date
from django.utils import timezone


class BookSlotTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.book_slot_url = reverse("book_slot")
        self.test_date = date(timezone.now().year + 1, 7, 16)

        self.event = Event.objects.create(
            name="La fin du monde",
            event_date=self.test_date,
        )

        self.plage = Plage.objects.create(
            event=self.event,
            name="beach",
            start_time="08:00:00",
            end_time="17:00:00",
            slot_duration_minutes=10,
            break_start_time="12:00:00",
            break_end_time="13:00:00",
            is_active=True,
        )
        self.valid_data = {
            "plage": self.plage.pk,
            "startAt": f"{self.test_date}T08:08:00Z",
            "endAt": f"{self.test_date}T08:28:00Z",
            "clientFname": "Henry B.",
            "clientLname": "Belton",
            "clientEmail": "testidootest@gmail.com",
            "clientPhone": "123-456-7890",
            "item": "cerveau",
            "itemDescription": "Mon cerveau est parti à la course, ça m'en prend un nouveau",
            "liabilityAccepted": True,
        }

    def test_book_slot_success_returns_201(self):
        resp = self.client.post(
            self.book_slot_url,
            data=self.valid_data,
            format="json",
        )
        self.assertEqual(resp.status_code, 201)

    def test_book_slot_success_returns_correct_fields(self):
        resp = self.client.post(
            self.book_slot_url,
            data=self.valid_data,
            format="json",
        )
        body = resp.json()
        self.assertIn("id", body)
        self.assertIn("plage", body)
        self.assertIn("startAt", body)
        self.assertIn("endAt", body)
        self.assertIn("clientFname", body)
        self.assertIn("clientLname", body)
        self.assertIn("clientEmail", body)
        self.assertIn("clientPhone", body)
        self.assertIn("item", body)
        self.assertIn("itemDescription", body)
        self.assertIn("liabilityAccepted", body)
        self.assertIn("isCanceled", body)
        self.assertIn("updatedAt", body)
        self.assertIn("createdAt", body)
        self.assertEqual(body["plage"], self.plage.pk)
        self.assertEqual(body["startAt"], f"{self.test_date}T08:08:00Z")
        self.assertEqual(body["endAt"], f"{self.test_date}T08:28:00Z")
        self.assertEqual(body["clientFname"], "Henry B.")
        self.assertEqual(body["clientLname"], "Belton")
        self.assertEqual(body["clientEmail"], "testidootest@gmail.com")
        self.assertEqual(body["clientPhone"], "123-456-7890")
        self.assertEqual(body["item"], "cerveau")
        self.assertEqual(body["itemDescription"], "Mon cerveau est parti à la course, ça m'en prend un nouveau")
        self.assertEqual(body["liabilityAccepted"], True)
        self.assertEqual(body["isCanceled"], False)

    # ── Authentification ─────────────────────────────────────

    # aucun test ici car aucun besoin d'authentification

    # ── Validation ───────────────────────────────────────────

    def test_book_slot_missing_required_fields_return_400(self):
        required_fields = [
            "plage",
            "startAt",
            "endAt",
            "clientFname",
            "clientLname",
            "clientEmail",
            "clientPhone",
            "item",
            "itemDescription",
            "liabilityAccepted",
        ]
        for field in required_fields:
            with self.subTest(field=field):
                data = {**self.valid_data}
                del data[field]
                resp = self.client.post(self.book_slot_url, data=data, format="json")
                self.assertEqual(resp.status_code, 400)
                self.assertIn(field, resp.json())

    def test_book_slot_invalid_email_returns_400(self):
        data = {**self.valid_data, "clientEmail": "not-an-email"}
        resp = self.client.post(self.book_slot_url, data=data, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("clientEmail", resp.json())

    def test_book_slot_invalid_plage_returns_400(self):
        data = {**self.valid_data, "plage": 99999}
        resp = self.client.post(self.book_slot_url, data=data, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("plage", resp.json())

    def test_book_slot_duplicate_plage_and_start_at_returns_400(self):
        first = self.client.post(self.book_slot_url, data=self.valid_data, format="json")
        self.assertEqual(first.status_code, 201)
        resp = self.client.post(self.book_slot_url, data=self.valid_data, format="json")
        self.assertEqual(resp.status_code, 400)

    def test_book_slot_overlap_same_plage_returns_400(self):
        first_data = {**self.valid_data, "startAt": f"{self.test_date} 09:00:00", "endAt": f"{self.test_date} 09:20:00",}
        overlap_data = {
            **self.valid_data,
            "startAt": f"{self.test_date} 09:10:00",
            "endAt": f"{self.test_date} 09:30:00",
            "clientEmail": "other@test.com",
        }
        first = self.client.post(self.book_slot_url, data=first_data, format="json")
        self.assertEqual(first.status_code, 201)
        resp = self.client.post(self.book_slot_url, data=overlap_data, format="json")
        self.assertEqual(resp.status_code, 400)