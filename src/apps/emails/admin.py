from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.common.admin import ModelAdmin
from apps.emails.models import EmailThread
from apps.emails.utils import render_colored_email_status_html


@admin.register(EmailThread)
class EmailThreadAdmin(ModelAdmin):
    list_display = (
        "__str__",
        "subject",
        "recipient",
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
    fieldsets = (
        (None, {
            "fields": (
                "id",
                "subject",
                "recipient",
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

    @admin.display(description=_("status"))
    def colored_status(self, obj: EmailThread = None) -> str:
        return "-" if not obj else render_colored_email_status_html(email_thread=obj)
