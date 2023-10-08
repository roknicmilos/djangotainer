from threading import Thread
from unittest.mock import patch

from django.template.loader import get_template
from django.utils.html import strip_tags

from apps.common.tests import TestCase
from apps.emails.models import Email
from apps.emails.tests.factories import EmailFactory


class TestEmail(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.email = EmailFactory()

    def test_email_str_method(self):
        expected_str = f'"{self.email.subject}" email'
        self.assertEqual(str(self.email), expected_str)

    @patch.object(Thread, "start")
    def test_should_start_thread_for_sending_the_email(self, mock_start):
        self.email.send()
        mock_start.assert_called_once()

    @patch.object(Email, "_do_send_email", return_value=1)
    def test_should_succeed_to_send_email(self, mock_do_sent_email):
        self.email._send_email()
        self.assertEqual(self.email.status, Email.Statuses.SUCCESS)
        self.assertEqual(self.email.error, "")
        mock_do_sent_email.assert_called_once()

    @patch.object(Email, "_do_send_email")
    def test_should_fail_to_send_email(self, mock_do_sent_email):
        # When email wasn't sent for some reason:
        mock_do_sent_email.return_value = 0
        self.email._send_email()
        self.assertEqual(self.email.status, Email.Statuses.FAILURE)
        self.assertEqual(self.email.error, "Email was not sent")
        mock_do_sent_email.assert_called_once()

        mock_do_sent_email.reset_mock()

        # When sending the email raised an error:
        mock_do_sent_email.side_effect = ValueError("Something went wrong")
        self.email._send_email()
        self.assertEqual(self.email.status, Email.Statuses.FAILURE)
        self.assertEqual(self.email.error, "Something went wrong")
        mock_do_sent_email.assert_called_once()

    @patch("apps.emails.models.send_mail")
    @patch.object(Email, "_render_html_message")
    def test_should_html_and_send_mail(self, mock_render_html_message, mock_send_mail):
        html_message = "<div>Email HTML</div>"
        mock_render_html_message.return_value = html_message

        self.email._do_send_email()

        mock_render_html_message.assert_called_once()
        mock_send_mail.assert_called_once_with(
            subject=self.email.subject,
            message=strip_tags(html_message),
            from_email=self.email.email_from,
            recipient_list=[self.email.recipient],
            html_message=html_message,
        )

    def test_should_render_html_message(self):
        template = get_template(EmailFactory.template_path)
        expected_html = template.render(self.email.context)

        actual_html = self.email._render_html_message()

        self.assertEqual(actual_html, expected_html)
