from unittest.mock import patch

from django.contrib.admin.sites import site as admin_site
from django.contrib.auth import get_user_model
from django.contrib.messages import constants as messages_constants
from faker import Faker

from apps.common.tests import TestCase
from apps.common.utils import get_model_admin_change_details_url
from apps.emails.admin import EmailAdmin
from apps.emails.models import Email
from apps.emails.tests.factories import EmailFactory


class TestEmailAdmin(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_model = get_user_model()

    def setUp(self) -> None:
        super().setUp()
        self.email_admin = EmailAdmin(
            model=Email,
            admin_site=admin_site
        )

    def test_should_not_be_editable_model_admin(self):
        request = self.get_request_example()
        has_change_permission = self.email_admin.has_change_permission(request=request)
        self.assertIs(has_change_permission, False)

    @patch("apps.emails.admin.render_colored_email_status_html")
    def test_should_return_colored_status(self, mock_render_colored_email_status_html):
        mock_render_colored_email_status_html.return_value = "<div>colored label</div>"

        # When Email instance is not passed:
        colored_status = self.email_admin.colored_status()
        self.assertEqual(colored_status, "-")
        mock_render_colored_email_status_html.assert_not_called()

        # When Email instance is passed:
        email = EmailFactory()
        colored_status = self.email_admin.colored_status(obj=email)
        self.assertEqual(colored_status, mock_render_colored_email_status_html.return_value)
        mock_render_colored_email_status_html.assert_called_once_with(email=email)

    def test_should_return_single_dash_when_user_recipient_does_not_exist(self):
        email = Faker().email()
        self.assertFalse(self.user_model.objects.filter(email=email).exists())

        # When Email instance is not passed:
        recipient_user = self.email_admin.recipient_user()
        self.assertEqual(recipient_user, "-")

        # When Email instance is passed:
        email = EmailFactory(recipient=email)
        recipient_user = self.email_admin.recipient_user(obj=email)
        self.assertEqual(recipient_user, "-")

    def test_should_return_single_link_to_user_recipient_when_they_exist(self):
        email_address = Faker().email()
        user = self.user_model.objects.create(email=email_address)
        email = EmailFactory(recipient=email_address)
        recipient_user = self.email_admin.recipient_user(obj=email)
        href = get_model_admin_change_details_url(obj=user)
        expected_recipient_user = f'<a href="{href}">{email_address}</a>'
        self.assertEqual(recipient_user, expected_recipient_user)

    @patch.object(Email, "send")
    def test_should_send_5_emails_and_print_success_message(self, mock_send):
        emails_count = 5
        EmailFactory.create_batch(size=emails_count)
        queryset = Email.objects.all()
        self.assertEqual(queryset.count(), emails_count)
        request = self.get_request_example()
        self.email_admin.send_emails(request=request, queryset=queryset)
        self.assertEqual(mock_send.call_count, emails_count)

        self.assertMessages(
            request=request,
            message=f"Successfully sent {emails_count} emails.",
            level=messages_constants.SUCCESS
        )

    @patch.object(Email, "send")
    def test_should_not_send_more_than_5_emails_and_should_print_error_message(self, mock_send):
        emails_count = 6
        EmailFactory.create_batch(size=emails_count)
        queryset = Email.objects.all()
        self.assertEqual(queryset.count(), emails_count)
        request = self.get_request_example()
        self.email_admin.send_emails(request=request, queryset=queryset)
        self.assertEqual(mock_send.call_count, 0)

        expected_message = (
            "You can select a maximum of 5 emails to send at once. "
            "Please reduce the number of selected emails and try again."
        )
        self.assertMessages(
            request=request,
            message=expected_message,
            level=messages_constants.ERROR
        )
