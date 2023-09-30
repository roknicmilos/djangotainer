from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.common.admin import ModelAdmin
from apps.common.utils import get_model_admin_change_details_url
from apps.emails.models import EmailThread
from apps.emails.utils import render_colored_email_status_html
from apps.users.models import User


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
        if obj and (user := User.objects.filter(email=obj.recipient).first()):
            href = get_model_admin_change_details_url(obj=user)
            return mark_safe(f'<a href="{href}">{user.email}</a>')
        return "-"

    @admin.display(description=_("status"))
    def colored_status(self, obj: EmailThread = None) -> str:
        return render_colored_email_status_html(email_thread=obj) if obj else "-"
