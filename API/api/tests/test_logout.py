from api.tests.base_TestClass import BaseAPITestCase


class LogoutTests(BaseAPITestCase):
    def test_logout_requires_auth_when_not_logged_in(self):
        resp = self.client.post(self.logout_url, format="json")
        self.assertEqual(resp.status_code, 401)

    def test_logout_clears_jwt_cookies(self):
        self.login_and_set_cookies()

        self.assertIn("access_token", self.client.cookies)
        self.assertIn("refresh_token", self.client.cookies)

        resp = self.client.post(self.logout_url, format="json")

        self.assertEqual(resp.status_code, 200)
        self.assertIn("access_token", resp.cookies)
        self.assertIn("refresh_token", resp.cookies)

        self.assertIn(resp.cookies["access_token"]["max-age"], ("0", 0))
        self.assertIn(resp.cookies["refresh_token"]["max-age"], ("0", 0))

    def test_after_logout_me_is_unauthorized(self):
        self.login_and_set_cookies()

        me_resp = self.client.get(self.me_url)
        self.assertEqual(me_resp.status_code, 200)

        self.client.post(self.logout_url, format="json")
        self.clear_jwt_cookies()

        me_resp2 = self.client.get(self.me_url)
        self.assertEqual(me_resp2.status_code, 401)