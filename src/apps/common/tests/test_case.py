from django.core.handlers.wsgi import WSGIRequest
from django.test import Client, TestCase as BaseTestCase
from django.contrib.auth import get_user_model


class TestCase(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = Client()

    def get_request_example(self, url_query_params: dict = None) -> WSGIRequest:
        requests = self.client.get(path="/", data=url_query_params).wsgi_request
        if url_query_params:
            requests.query_params = url_query_params
        return requests

    def create_and_login_superuser(self) -> None:
        credentials = {"email": "superuser@example.com", "password": "password"}
        get_user_model().objects.create_superuser(**credentials)
        if not self.client.login(**credentials):
            self.fail("Failed to login superuser")
