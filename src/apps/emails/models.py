from threading import Thread
from django.conf import settings
from django.template.loader import get_template
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.db import models

from apps.common.models import BaseModel


class EmailThread(BaseModel):
    class Meta:
        verbose_name = _("Email Thread")
        verbose_name_plural = _("Email Threads")

    email_from = settings.EMAIL_HOST_USER

    class Statuses(models.TextChoices):
        PENDING = "pending", _("waiting to send email")
        SUCCESS = "success", _("successfully sent email")
        FAILURE = "failure", _("failed to send email")

    subject = models.CharField(
        verbose_name=_("email subject"),
        max_length=250,
    )
    recipient = models.CharField(
        verbose_name=_("recipient email address"),
        max_length=250,
    )
    context = models.JSONField(
        verbose_name=_("email context"),
        default=dict,
    )
    template_path = models.CharField(
        verbose_name=_("template path"),
        max_length=250,
    )
    category = models.CharField(
        verbose_name=_("category"),
        max_length=250,
        default="general",
        help_text=_("For easier grouping and searching of specific emails"),
    )
    status = models.CharField(
        verbose_name=_("status"),
        max_length=10,
        choices=Statuses.choices,
        default=Statuses.PENDING,
        help_text=_(
            "Note that the email can successfully be sent even "
            "if the recipient email address does not exist"
        ),
    )
    error = models.TextField(
        verbose_name=_("error"),
        default="",
        help_text=_("An error occurred during the email sending process")
    )

    def __str__(self):
        return f'"{self.subject}" email'

    def start(self) -> None:
        Thread(target=self.send_email).start()

    def send_email(self) -> None:
        try:
            sent_email_count = self._do_send_email()
        except Exception as error:
            self.update(
                status=self.Statuses.FAILURE,
                error=str(error)
            )
        else:
            self.update(
                status=self.Statuses.SUCCESS if sent_email_count else self.Statuses.FAILURE,
                error="" if sent_email_count else "Email was not sent",
            )

    def _do_send_email(self) -> int:
        html_message = self._render_html_message()
        return send_mail(
            subject=self.subject,
            message=strip_tags(html_message),
            from_email=self.email_from,
            recipient_list=[self.recipient],
            html_message=html_message,
        )

    def _render_html_message(self) -> str:
        template = get_template(self.template_path)
        return template.render(self.context)
