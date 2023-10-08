from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.common.admin import ModelAdmin
from apps.common.utils import get_model_admin_change_details_url
from apps.emails.models import EmailThread
from apps.emails.utils import render_colored_email_status_html


@admin.register(EmailThread)
class EmailThreadAdmin(ModelAdmin):
    list_display = (
        "__str__",
        "subject",
        "recipient",
        "recipient_user",
        "colored_status",
        "category",
    )
    search_fields = (
        "subject",
        "recipient",
        "category",
    )
    list_filter = (
        "status",
    )
    actions = (
        "send_emails",
    )
    fieldsets = (
        (None, {
            "fields": (
                "id",
                "subject",
                "recipient",
                "recipient_user",
                "colored_status",
            )
        }),
        (_("Details"), {
            "fields": (
                "context",
                "template_path",
                "status",
                "error",
                "category",
            )
        },),
    )

    def has_change_permission(self, request, obj: EmailThread = None) -> bool:
        return False

    @admin.display(description=_("recipient user"))
    def recipient_user(self, obj: EmailThread = None) -> str:
        user_model = get_user_model()
        if obj and (user := user_model.objects.filter(email=obj.recipient).first()):
            href = get_model_admin_change_details_url(obj=user)
            return mark_safe(f'<a href="{href}">{user.email}</a>')
        return "-"

    @admin.display(description=_("status"))
    def colored_status(self, obj: EmailThread = None) -> str:
        return render_colored_email_status_html(email_thread=obj) if obj else "-"

    @admin.action(description=_("Send selected emails"))
    def send_emails(self, request: WSGIRequest, queryset: QuerySet) -> None:
        emails_count = queryset.count()
        if emails_count <= 5:
            _do_send_emails(
                request=request,
                queryset=queryset
            )
        else:
            _display_send_emails_error_message(
                request=request,
                selected_emails_count=emails_count
            )


def _do_send_emails(request: WSGIRequest, queryset: QuerySet) -> None:
    emails_count = queryset.count()
    for email_thread in queryset:
        email_thread.start()
    message = _("Successfully sent {emails_count} {label}.").format(
        emails_count=emails_count,
        label=_("emails") if emails_count > 1 else _("email")
    )
    messages.success(
        request=request,
        message=message
    )


def _display_send_emails_error_message(request: WSGIRequest, selected_emails_count: int) -> None:
    message = _(
        "You can select a maximum of 5 emails to send at once. "
        "Please reduce the number of selected emails and try again."
    ).format(
        emails_count=selected_emails_count
    )
    messages.error(
        request=request,
        message=message
    )
