from os.path import join
from threading import Thread
from unittest.mock import patch

from django.conf import settings
from django.template.loader import get_template
from django.test import override_settings
from django.utils.html import strip_tags

from apps.common.tests import TestCase
from apps.emails.models import EmailThread
from apps.emails.tests.factories import EmailThreadFactory


class TestEmailThread(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.email_thread = EmailThreadFactory()

    def test_email_thread_str_method(self):
        expected_str = f'"{self.email_thread.subject}" email'
        self.assertEqual(str(self.email_thread), expected_str)

    @patch.object(Thread, "start")
    def test_should_start_thread_for_sending_the_email(self, mock_start):
        self.email_thread.start()
        mock_start.assert_called_once()

    @patch.object(EmailThread, "_do_send_email", return_value=1)
    def test_should_succeed_to_send_email(self, mock_do_sent_email):
        self.email_thread.send_email()
        self.assertEqual(self.email_thread.status, EmailThread.Statuses.SUCCESS)
        self.assertEqual(self.email_thread.error, "")
        mock_do_sent_email.assert_called_once()

    @patch.object(EmailThread, "_do_send_email")
    def test_should_fail_to_send_email(self, mock_do_sent_email):
        # When email wasn't sent for some reason:
        mock_do_sent_email.return_value = 0
        self.email_thread.send_email()
        self.assertEqual(self.email_thread.status, EmailThread.Statuses.FAILURE)
        self.assertEqual(self.email_thread.error, "Email was not sent")
        mock_do_sent_email.assert_called_once()

        mock_do_sent_email.reset_mock()

        # When sending the email raised an error:
        mock_do_sent_email.side_effect = ValueError("Something went wrong")
        self.email_thread.send_email()
        self.assertEqual(self.email_thread.status, EmailThread.Statuses.FAILURE)
        self.assertEqual(self.email_thread.error, "Something went wrong")
        mock_do_sent_email.assert_called_once()

    @patch("apps.emails.models.send_mail")
    @patch.object(EmailThread, "_render_html_message")
    def test_should_html_and_send_mail(self, mock_render_html_message, mock_send_mail):
        html_message = "<div>Email HTML</div>"
        mock_render_html_message.return_value = html_message

        self.email_thread._do_send_email()

        mock_render_html_message.assert_called_once()
        mock_send_mail.assert_called_once_with(
            subject=self.email_thread.subject,
            message=strip_tags(html_message),
            from_email=self.email_thread.email_from,
            recipient_list=[self.email_thread.recipient],
            html_message=html_message,
        )

    @override_settings(
        TEMPLATES=[
            {
                **settings.TEMPLATES[0],
                "DIRS": [
                    join(settings.PROJECT_ROOT, "apps", "emails", "tests"),
                ],
            }
        ]
    )
    def test_should_render_html_message(self):
        template = get_template(EmailThreadFactory.template_path)
        expected_html = template.render(self.email_thread.context)

        actual_html = self.email_thread._render_html_message()

        self.assertEqual(actual_html, expected_html)
