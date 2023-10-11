from django.contrib.auth import get_user_model
from django.contrib.messages import constants as messages_constants
from django.contrib.messages import get_messages
from django.core.handlers.wsgi import WSGIRequest
from django.test import Client
from django.test import TestCase as BaseTestCase


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

    def assertMessages(self, request: WSGIRequest, message: str, level: int, index: int = 0) -> None:
        """
        Asserts a messages expected to be added to the
        request object via django.contrib.messages module
        """

        messages = list(get_messages(request))
        message_obj = messages[index]
        expected_tas = messages_constants.DEFAULT_TAGS.get(level)
        self.assertEqual(message_obj.tags, expected_tas)
        self.assertEqual(message_obj.level, level)
        self.assertEqual(message_obj.message, message)
