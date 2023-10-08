from django.conf import settings
from django.urls import translate_url
from django.utils import translation


class TranslatedURL:

    def __init__(self, url_path: str, lang_code: str, lang_label: str):
        self.lang_code = lang_code
        with translation.override(language=lang_code):
            self.lang_label = str(lang_label)
        self.url = translate_url(url=url_path, lang_code=lang_code)

    @classmethod
    def create_batch(cls, url_path: str) -> list["TranslatedURL"]:
        translation_urls = []
        for lang_code, lang_label in settings.LANGUAGES:
            translation_urls.append(
                TranslatedURL(
                    url_path=url_path,
                    lang_code=lang_code,
                    lang_label=lang_label
                )
            )

        return translation_urls
