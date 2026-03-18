from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient

from api.models import User


@override_settings(JWT_COOKIE_SECURE=False, JWT_COOKIE_SAMESITE="Lax")
class BaseAPITestCase(TestCase):
    default_username = "admin1"
    default_password = "pass123"
    default_email = "admin1@test.com"

    def setUp(self):
        super().setUp()
        self.client = APIClient()

        self.user = User.objects.create(
            username=self.default_username,
            password_hash=make_password(self.default_password),
            email=self.default_email,
        )

        try:
            self.login_url = reverse("login")
        except Exception:
            self.login_url = "/api/login/"

        try:
            self.me_url = reverse("me")
        except Exception:
            self.me_url = "/api/user/me/"

        try:
            self.logout_url = reverse("logout")
        except Exception:
            self.logout_url = "/api/logout/"

    def login_and_set_cookies(
        self,
        username: str | None = None,
        password: str | None = None,
    ):
        username = username or self.default_username
        password = password or self.default_password

        resp = self.client.post(
            self.login_url,
            data={"username": username, "password": password},
            format="json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("access_token", resp.cookies)
        self.assertIn("refresh_token", resp.cookies)

        self.client.cookies["access_token"] = resp.cookies["access_token"].value
        self.client.cookies["refresh_token"] = resp.cookies["refresh_token"].value
        return resp

    def clear_jwt_cookies(self):
        self.client.cookies.clear()