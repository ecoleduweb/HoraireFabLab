from api.tests.base_TestClass import BaseAPITestCase

class LoginTests(BaseAPITestCase):
    def test_login_success_sets_cookies_and_returns_username_only(self):
        resp = self.client.post(
            self.login_url,
            data={"username": "admin1", "password": "pass123"},
            format="json",
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"username": "admin1"})

        body = resp.json()
        self.assertNotIn("tokens", body)
        self.assertNotIn("access", body)
        self.assertNotIn("refresh", body)

        self.assertIn("access_token", resp.cookies)
        self.assertIn("refresh_token", resp.cookies)

    def test_login_missing_fields_returns_400(self):
        resp = self.client.post(
            self.login_url, 
            data={"username": "admin1"}, 
            format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("detail", resp.json())

    def test_login_wrong_password_returns_401(self):
        resp = self.client.post(
            self.login_url,
            data={"username": "admin1", "password": "wrong"},
            format="json",
        )
        self.assertEqual(resp.status_code, 401)

    def test_login_unknown_user_returns_401(self):
        resp = self.client.post(
            self.login_url,
            data={"username": "nope", "password": "pass123"},
            format="json",
        )
        self.assertEqual(resp.status_code, 401)

    def test_login_ignores_invalid_access_cookie(self):
        self.client.cookies["access_token"] = "invalid.token.value"
        resp = self.client.post(
            self.login_url,
            data={"username": "admin1", "password": "pass123"},
            format="json",
        )
        self.assertEqual(resp.status_code, 200)