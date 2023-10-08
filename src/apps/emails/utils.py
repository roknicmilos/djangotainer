from django.utils.safestring import mark_safe

from apps.emails.models import Email


def render_colored_email_status_html(email: Email) -> str:
    colors_map = {
        Email.Statuses.PENDING: ("#e0e0e0", "black"),
        Email.Statuses.SUCCESS: ("#def7d9", "green"),
        Email.Statuses.FAILURE: ("#f7d9d9", "red"),
    }

    background_color, text_color = colors_map.get(email.status)

    style = (
        f"color: {text_color};"
        f"background-color: {background_color};"
        "text-align: center;"
        "border-radius: 5px;"
        "padding: 1px 3px;"
        "min-width: 75px;"
        "width: fit-content;"
    )

    return mark_safe(f'<div style="{style}">{email.status}</div>')
