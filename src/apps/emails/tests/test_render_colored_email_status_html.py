from apps.common.tests import TestCase
from apps.emails.models import Email
from apps.emails.tests.factories import EmailFactory
from apps.emails.utils import render_colored_email_status_html


class TestRenderColoredEmailStatusHTML(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.email = EmailFactory()

    def test_should_render_colored_email_pending_status_html(self):
        self.email.update(status=Email.Statuses.PENDING.value)
        self.assertEqualColoredStatusHTML(text_color="black", background_color="#e0e0e0")

    def test_should_render_colored_email_success_status_html(self):
        self.email.update(status=Email.Statuses.SUCCESS.value)
        self.assertEqualColoredStatusHTML(text_color="green", background_color="#def7d9")

    def test_should_render_colored_email_failure_status_html(self):
        self.email.update(status=Email.Statuses.FAILURE.value)
        self.assertEqualColoredStatusHTML(text_color="red", background_color="#f7d9d9")

    def assertEqualColoredStatusHTML(self, text_color: str, background_color: str) -> None:
        actual_html = render_colored_email_status_html(email=self.email)
        expected_style = (
            f"color: {text_color};"
            f"background-color: {background_color};"
            "text-align: center;"
            "border-radius: 5px;"
            "padding: 1px 3px;"
            "min-width: 75px;"
            "width: fit-content;"
        )
        expected_html = f'<div style="{expected_style}">{self.email.status}</div>'
        self.assertEqual(actual_html, expected_html)
