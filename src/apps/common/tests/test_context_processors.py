from unittest.mock import patch

from apps.common.context_processors import i18n
from apps.common.models import TranslatedURL
from apps.common.tests import TestCase


class TestContextProcessors(TestCase):

    @patch("apps.common.context_processors.base_i18n", return_value={})
    @patch.object(TranslatedURL, "create_batch", return_value=[])
    def test_should_add_translated_urls_to_context(self, mock_create_batch, mock_base_i18n):
        request = self.get_request_example()
        context = i18n(request=request)
        mock_base_i18n.assert_called_once_with(request=request)
        mock_create_batch.assert_called_once_with(url_path=request.path_info)
        self.assertEqual(context, {"translated_urls": []})
