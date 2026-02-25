from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient

from api.models import User
from api.tests.base_TestClass import BaseAPITestCase


@override_settings(JWT_COOKIE_SECURE=False, JWT_COOKIE_SAMESITE="Lax")
class MeTests(TestCase, BaseAPITestCase):
    def setUp(self):
        self.client = APIClient()
        User.objects.create(
            username="admin1",
            password_hash=make_password("pass123"),
            email="admin1@test.com",
        )

        try:
            self.login_url = reverse("login")
        except Exception:
            self.login_url = "/api/login/"

        try:
            self.me_url = reverse("me")
        except Exception:
            self.me_url = "/api/user/me/"

    def test_me_requires_auth(self):
        resp = self.client.get(self.me_url)
        self.assertIn(resp.status_code, (401, 403))

    def test_me_returns_username_when_logged_in(self):
        self.login_and_set_cookies(self.login_url, "admin1", "pass123")

        resp = self.client.get(self.me_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"username": "admin1"})

    def test_me_fails_with_invalid_token_cookie(self):
        self.client.cookies["access_token"] = "invalid.token.value"

        resp = self.client.get(self.me_url)
        self.assertIn(resp.status_code, (401, 403))

    def test_me_after_logout_is_unauthorized(self):
        self.login_and_set_cookies(self.login_url, "admin1", "pass123")

        # logout stateless = supprimer cookies
        self.client.cookies.clear()

        resp = self.client.get(self.me_url)
        self.assertIn(resp.status_code, (401, 403))