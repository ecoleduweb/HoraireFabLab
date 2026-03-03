from api.tests.base_TestClass import BaseAPITestCase

class MeTests(BaseAPITestCase):
    def test_me_requires_auth(self):
        resp = self.client.get(self.me_url)
        self.assertIn(resp.status_code, (401, 403))

    def test_me_returns_username_when_logged_in(self):
        self.login_and_set_cookies()
        resp = self.client.get(self.me_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"username": "admin1"})

    def test_me_after_logout_is_unauthorized(self):
        self.login_and_set_cookies()
        self.clear_jwt_cookies()
        resp = self.client.get(self.me_url)
        self.assertIn(resp.status_code, (401, 403))