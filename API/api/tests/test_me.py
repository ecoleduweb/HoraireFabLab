from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient

from api.models import User


@override_settings(
    JWT_COOKIE_SECURE=False,
    JWT_COOKIE_SAMESITE="Lax",
)
class MeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username="admin1",
            password_hash=make_password("pass123"),
            email="admin1@test.com",
        )

        # URL login
        try:
            self.login_url = reverse("login")
        except Exception:
            self.login_url = "/api/login/"

        # URL me
        try:
            self.me_url = reverse("me")
        except Exception:
            self.me_url = "/api/user/me/"

    def _login_and_set_cookies(self):
        """Helper: login et réinjecte les cookies dans le client pour les requêtes suivantes."""
        resp = self.client.post(
            self.login_url,
            data={"username": "admin1", "password": "pass123"},
            format="json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("access_token", resp.cookies)
        self.assertIn("refresh_token", resp.cookies)

        #  copie les cookies de la réponse vers le client
        self.client.cookies["access_token"] = resp.cookies["access_token"].value
        self.client.cookies["refresh_token"] = resp.cookies["refresh_token"].value

    def test_me_requires_auth(self):
        """Sans cookie access_token, /me doit refuser."""
        resp = self.client.get(self.me_url)
        self.assertIn(resp.status_code, (401, 403))  

    def test_me_returns_username_when_logged_in(self):
        """Après login (cookie access_token), /me retourne le username (claim JWT)."""
        self._login_and_set_cookies()

        resp = self.client.get(self.me_url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"username": "admin1"})

    def test_me_fails_with_invalid_token_cookie(self):
        """Si access_token cookie invalide, /me doit refuser."""
        self.client.cookies["access_token"] = "invalid.token.value"

        resp = self.client.get(self.me_url)
        self.assertIn(resp.status_code, (401, 403))

    def test_me_after_logout_is_unauthorized(self):
       
        self._login_and_set_cookies()

        self.client.cookies.clear()
        # vider cookies JWT
        self.client.cookies.pop("access_token", None)
        self.client.cookies.pop("refresh_token", None)

        resp = self.client.get(self.me_url)
        self.assertIn(resp.status_code, (401, 403))