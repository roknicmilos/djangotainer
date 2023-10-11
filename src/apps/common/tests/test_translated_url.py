from django.conf import settings
from django.urls import reverse, translate_url
from django.utils import translation

from apps.common.models import TranslatedURL
from apps.common.tests import TestCase


class TestTranslatedURL(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url_path = reverse("admin:index")

    def test_should_create_translated_url_for_single_language(self):
        lang_code, lang_label = settings.LANGUAGES[0]
        translation_url = TranslatedURL(
            url_path=self.url_path,
            lang_code=lang_code,
            lang_label=lang_label
        )
        self.assertTranslatedURL(
            translation_url=translation_url,
            lang_code=lang_code,
            lang_label=lang_label
        )

    def test_should_create_translated_url_for_all_languages(self):
        translated_urls = TranslatedURL.create_batch(url_path=self.url_path)
        languages = settings.LANGUAGES
        self.assertEqual(len(translated_urls), len(languages))
        for translation_url, (lang_code, lang_label) in zip(translated_urls, languages):
            self.assertTranslatedURL(
                translation_url=translation_url,
                lang_code=lang_code,
                lang_label=lang_label
            )

    def assertTranslatedURL(self, translation_url: TranslatedURL, lang_code: str, lang_label: str) -> None:
        self.assertEqual(translation_url.lang_code, lang_code)
        with translation.override(language=lang_code):
            translated_lang_label = str(lang_label)
        self.assertEqual(translation_url.lang_label, translated_lang_label)
        expected_url = translate_url(url=self.url_path, lang_code=lang_code)
        self.assertEqual(translation_url.url, expected_url)
