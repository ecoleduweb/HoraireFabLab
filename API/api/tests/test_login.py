from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient

from api.models import User


@override_settings(
    JWT_COOKIE_SECURE=False,      # en test, on force secure=False
    JWT_COOKIE_SAMESITE="Lax",
)
class LoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username="admin1",
            password_hash=make_password("pass123"),
            email="admin1@test.com",
        )

        # Si reverse("login") ne marche pas chez toi, remplace par "/api/login/"
        try:
            self.url = reverse("login")
        except Exception:
            self.url = "/api/login/"

    def test_login_success_sets_cookies_and_returns_username_only(self):
        resp = self.client.post(
            self.url,
            data={"username": "admin1", "password": "pass123"},
            format="json",
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"username": "admin1"})

        #  tokens ne doivent pas être dans le body
        body = resp.json()
        self.assertNotIn("tokens", body)
        self.assertNotIn("access", body)
        self.assertNotIn("refresh", body)

        #  cookies présents
        self.assertIn("access_token", resp.cookies)
        self.assertIn("refresh_token", resp.cookies)

        access_cookie = resp.cookies["access_token"]
        refresh_cookie = resp.cookies["refresh_token"]

        #  HttpOnly
        self.assertTrue(access_cookie["httponly"])
        self.assertTrue(refresh_cookie["httponly"])

        #  SameSite
        self.assertEqual(access_cookie["samesite"], "Lax")
        self.assertEqual(refresh_cookie["samesite"], "Lax")

        #  Secure (forcé à False via override_settings)
        self.assertFalse(access_cookie["secure"])
        self.assertFalse(refresh_cookie["secure"])

        # les Valeur non vide
        self.assertTrue(access_cookie.value)
        self.assertTrue(refresh_cookie.value)

    def test_login_missing_fields_returns_400(self):
        resp = self.client.post(self.url, data={"username": "admin1"}, format="json")
        self.assertEqual(resp.status_code, 400)

        # DRF renvoie généralement {"detail": "..."} dans ton service
        data = resp.json()
        self.assertIn("detail", data)

    def test_login_wrong_password_returns_401(self):
        resp = self.client.post(
            self.url,
            data={"username": "admin1", "password": "wrong"},
            format="json",
        )
        self.assertEqual(resp.status_code, 403)

    def test_login_unknown_user_returns_401(self):
        resp = self.client.post(
            self.url,
            data={"username": "nope", "password": "pass123"},
            format="json",
        )
        self.assertEqual(resp.status_code, 403)

    def test_login_ignores_invalid_access_cookie(self):
        """
        Vérifie que @authentication_classes([]) fait son job :
        même si un cookie access_token invalide traîne, /login fonctionne.
        """
        self.client.cookies["access_token"] = "invalid.token.value"

        resp = self.client.post(
            self.url,
            data={"username": "admin1", "password": "pass123"},
            format="json",
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"username": "admin1"})
        self.assertIn("access_token", resp.cookies)
        self.assertIn("refresh_token", resp.cookies)
