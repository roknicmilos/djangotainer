from django.core.handlers.wsgi import WSGIRequest
from django.template.context_processors import i18n as base_i18n

from apps.common.models import TranslatedURL


def i18n(request: WSGIRequest) -> dict:
    context = base_i18n(request=request)
    context["translated_urls"] = TranslatedURL.create_batch(url_path=request.path_info)
    return context
