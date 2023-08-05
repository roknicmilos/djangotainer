from django.core.handlers.wsgi import WSGIRequest
from django.test import Client, TestCase as BaseTestCase


class TestCase(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = Client()

    def get_request_example(self, url_query_params: dict = None) -> WSGIRequest:
        requests = self.client.get(path="/", data=url_query_params).wsgi_request
        if url_query_params:
            requests.query_params = url_query_params
        return requests
