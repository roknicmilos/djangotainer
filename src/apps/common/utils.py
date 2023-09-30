from django.db.models import Model
from django.urls import NoReverseMatch, reverse


def get_model_admin_change_details_url(obj: Model) -> str:
    from django.contrib.contenttypes.models import ContentType

    content_type = ContentType.objects.get_for_model(obj.__class__)
    try:
        view_name = f"admin:{content_type.app_label}_{content_type.model}_change"
        return reverse(viewname=view_name, args=(obj.id,))
    except NoReverseMatch:
        return ""
