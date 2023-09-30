from unittest.mock import patch

from django.contrib.admin.sites import site as admin_site

from apps.common.tests import TestCase
from apps.emails.admin import EmailThreadAdmin
from apps.emails.tests.factories import EmailThreadFactory
from apps.users.models import User


class TestEmailThreadAdmin(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.email_thread_admin = EmailThreadAdmin(model=User, admin_site=admin_site)

    def test_should_not_be_editable_model_admin(self):
        request = self.get_request_example()
        has_change_permission = self.email_thread_admin.has_change_permission(request=request)
        self.assertIs(has_change_permission, False)

    @patch("apps.emails.admin.render_colored_email_status_html")
    def test_should_return_colored_status(self, mock_render_colored_email_status_html):
        mock_render_colored_email_status_html.return_value = '<div>colored label</div>'

        # When EmailThread instance is not passed:
        colored_status = self.email_thread_admin.colored_status()
        self.assertEqual(colored_status, "-")
        mock_render_colored_email_status_html.assert_not_called()

        # When EmailThread instance is passed:
        email_thread = EmailThreadFactory()
        colored_status = self.email_thread_admin.colored_status(obj=email_thread)
        self.assertEqual(colored_status, mock_render_colored_email_status_html.return_value)
        mock_render_colored_email_status_html.assert_called_once_with(email_thread=email_thread)
