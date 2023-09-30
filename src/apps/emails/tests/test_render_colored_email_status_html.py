from apps.common.tests import TestCase
from apps.emails.models import EmailThread
from apps.emails.tests.factories import EmailThreadFactory
from apps.emails.utils import render_colored_email_status_html


class TestRenderColoredEmailStatusHTML(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.email_thread = EmailThreadFactory()
        cls.html_style_template = (
            f"color: @text_color;"
            f"background-color: @background_color;"
            "text-align: center;"
            "border-radius: 5px;"
            "padding: 1px 3px;"
            "min-width: 75px;"
            "width: fit-content;"
        )

    def test_should_render_colored_email_pending_status_html(self):
        self.assertEqual(self.email_thread.status, EmailThread.Statuses.PENDING.value)

        actual_html = render_colored_email_status_html(email_thread=self.email_thread)

        expected_style = (
            self.html_style_template
            .replace("@text_color", "black")
            .replace("@background_color", "#e0e0e0")
        )
        expected_html = f'<div style="{expected_style}">{self.email_thread.status}</div>'

        self.assertEqual(actual_html, expected_html)

    def test_should_render_colored_email_success_status_html(self):
        self.email_thread.update(status=EmailThread.Statuses.SUCCESS.value)

        actual_html = render_colored_email_status_html(email_thread=self.email_thread)

        expected_style = (
            self.html_style_template
            .replace("@text_color", "green")
            .replace("@background_color", "#def7d9")
        )
        expected_html = f'<div style="{expected_style}">{self.email_thread.status}</div>'

        self.assertEqual(actual_html, expected_html)

    def test_should_render_colored_email_failure_status_html(self):
        self.email_thread.update(status=EmailThread.Statuses.FAILURE.value)

        actual_html = render_colored_email_status_html(email_thread=self.email_thread)

        expected_style = (
            self.html_style_template
            .replace("@text_color", "red")
            .replace("@background_color", "#f7d9d9")
        )
        expected_html = f'<div style="{expected_style}">{self.email_thread.status}</div>'

        self.assertEqual(actual_html, expected_html)
