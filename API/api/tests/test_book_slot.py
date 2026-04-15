from api.tests.base_TestClass import BaseAPITestCase
from api.models import Slot, Plage, Event
from django.urls import reverse


class BookSlotTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.book_slot_url = reverse("book_slot")

        self.event = Event.objects.create(
            name="La fin du monde",
            event_date="2026-07-16",
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
            "start_at": "2026-07-16 08:08:00",
            "end_at": "2026-07-16 08:28:00",
            "client_fname": "Henry B.",
            "client_lname": "Belton",
            "client_email": "testidootest@gmail.com",
            "client_phone": "123-456-7890",
            "item": "cerveau",
            "item_description": "Mon cerveau est parti à la course, ça m'en prend un nouveau",
            "liability_accepted": True,
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
        self.assertIn("start_at", body)
        self.assertIn("end_at", body)
        self.assertIn("client_fname", body)
        self.assertIn("client_lname", body)
        self.assertIn("client_email", body)
        self.assertIn("client_phone", body)
        self.assertIn("item", body)
        self.assertIn("item_description", body)
        self.assertIn("liability_accepted", body)
        self.assertIn("is_canceled", body)
        self.assertIn("updated_at", body)
        self.assertIn("created_at", body)
        self.assertEqual(body["plage"], self.plage.pk)
        self.assertEqual(body["start_at"], "2026-07-16T08:08:00Z")
        self.assertEqual(body["end_at"], "2026-07-16T08:28:00Z")
        self.assertEqual(body["client_fname"], "Henry B.")
        self.assertEqual(body["client_lname"], "Belton")
        self.assertEqual(body["client_email"], "testidootest@gmail.com")
        self.assertEqual(body["client_phone"], "123-456-7890")
        self.assertEqual(body["item"], "cerveau")
        self.assertEqual(body["item_description"], "Mon cerveau est parti à la course, ça m'en prend un nouveau")
        self.assertEqual(body["liability_accepted"], True)
        self.assertEqual(body["is_canceled"], False)

    # ── Authentification ─────────────────────────────────────

    # aucun test ici car aucun besoin d'authentification

    # ── Validation ───────────────────────────────────────────

    def test_book_slot_missing_plage_returns_400(self):
        data = {**self.valid_data}
        del data["plage"]
        resp = self.client.post(self.book_slot_url, data=data, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("plage", resp.json())

    def test_book_slot_missing_start_at_returns_400(self):
        data = {**self.valid_data}
        del data["start_at"]
        resp = self.client.post(self.book_slot_url, data=data, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("start_at", resp.json())

    def test_book_slot_missing_end_at_returns_400(self):
        data = {**self.valid_data}
        del data["end_at"]
        resp = self.client.post(self.book_slot_url, data=data, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("end_at", resp.json())

    def test_book_slot_missing_client_fname_returns_400(self):
        data = {**self.valid_data}
        del data["client_fname"]
        resp = self.client.post(self.book_slot_url, data=data, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("client_fname", resp.json())

    def test_book_slot_missing_client_lname_returns_400(self):
        data = {**self.valid_data}
        del data["client_lname"]
        resp = self.client.post(self.book_slot_url, data=data, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("client_lname", resp.json())

    def test_book_slot_missing_client_email_returns_400(self):
        data = {**self.valid_data}
        del data["client_email"]
        resp = self.client.post(self.book_slot_url, data=data, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("client_email", resp.json())

    def test_book_slot_missing_client_phone_returns_400(self):
        data = {**self.valid_data}
        del data["client_phone"]
        resp = self.client.post(self.book_slot_url, data=data, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("client_phone", resp.json())

    def test_book_slot_missing_item_returns_400(self):
        data = {**self.valid_data}
        del data["item"]
        resp = self.client.post(self.book_slot_url, data=data, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("item", resp.json())

    def test_book_slot_missing_item_description_returns_400(self):
        data = {**self.valid_data}
        del data["item_description"]
        resp = self.client.post(self.book_slot_url, data=data, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("item_description", resp.json())

    def test_book_slot_missing_liability_accepted_returns_400(self):
        data = {**self.valid_data}
        del data["liability_accepted"]
        resp = self.client.post(self.book_slot_url, data=data, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("liability_accepted", resp.json())

    def test_book_slot_invalid_email_returns_400(self):
        data = {**self.valid_data, "client_email": "not-an-email"}
        resp = self.client.post(self.book_slot_url, data=data, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("client_email", resp.json())

    def test_book_slot_invalid_plage_returns_400(self):
        data = {**self.valid_data, "plage": 99999}
        resp = self.client.post(self.book_slot_url, data=data, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("plage", resp.json())

    def test_book_slot_duplicate_plage_and_start_at_returns_400(self):
        self.client.post(self.book_slot_url, data=self.valid_data, format="json")
        resp = self.client.post(self.book_slot_url, data=self.valid_data, format="json")
        self.assertEqual(resp.status_code, 400)
