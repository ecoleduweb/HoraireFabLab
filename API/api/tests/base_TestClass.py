from rest_framework.test import APIClient

class BaseAPITestCase:
    client: APIClient

    def login_and_set_cookies(
        self,
        login_url: str = "/api/login/",
        username: str = "admin1",
        password: str = "pass123",
    ) -> None:
        resp = self.client.post(
            login_url,
            data={"username": username, "password": password},
            format="json",
        )
        assert resp.status_code == 200
        self.client.cookies["access_token"] = resp.cookies["access_token"].value
        self.client.cookies["refresh_token"] = resp.cookies["refresh_token"].value