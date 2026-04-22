import os

from django.conf import settings
from django.test import TestCase


class SettingsTestCase(TestCase):
    """
    This class describes a settings test case.
    """

    def test_freeze_root_is_set(self):
        self.assertTrue(hasattr(settings, "FREEZE_ROOT"))
        self.assertTrue(os.path.isabs(settings.FREEZE_ROOT))

    def test_freeze_media_root_is_set(self):
        self.assertTrue(hasattr(settings, "FREEZE_MEDIA_ROOT"))
        self.assertEqual(settings.FREEZE_MEDIA_ROOT, settings.MEDIA_ROOT)

    def test_freeze_media_url_is_set(self):
        self.assertTrue(hasattr(settings, "FREEZE_MEDIA_URL"))
        self.assertEqual(settings.FREEZE_MEDIA_URL, settings.MEDIA_URL)

    def test_freeze_static_root_is_set(self):
        self.assertTrue(hasattr(settings, "FREEZE_STATIC_ROOT"))
        self.assertEqual(settings.FREEZE_STATIC_ROOT, settings.STATIC_ROOT)

    def test_freeze_static_url_is_set(self):
        self.assertTrue(hasattr(settings, "FREEZE_STATIC_URL"))
        self.assertEqual(settings.FREEZE_STATIC_URL, settings.STATIC_URL)

    def test_freeze_use_https_is_set(self):
        self.assertTrue(hasattr(settings, "FREEZE_USE_HTTPS"))
        self.assertIsInstance(settings.FREEZE_USE_HTTPS, bool)

    def test_freeze_protocol_is_set(self):
        self.assertTrue(hasattr(settings, "FREEZE_PROTOCOL"))
        self.assertIn(settings.FREEZE_PROTOCOL, ("http://", "https://"))

    def test_freeze_site_url_is_set(self):
        self.assertTrue(hasattr(settings, "FREEZE_SITE_URL"))

    def test_freeze_base_url_is_set(self):
        self.assertTrue(hasattr(settings, "FREEZE_BASE_URL"))
        self.assertEqual(settings.FREEZE_BASE_URL, "")

    def test_freeze_relative_urls_is_set(self):
        self.assertTrue(hasattr(settings, "FREEZE_RELATIVE_URLS"))
        self.assertFalse(settings.FREEZE_RELATIVE_URLS)

    def test_freeze_local_urls_is_set(self):
        self.assertTrue(hasattr(settings, "FREEZE_LOCAL_URLS"))
        self.assertFalse(settings.FREEZE_LOCAL_URLS)

    def test_freeze_follow_sitemap_urls_is_set(self):
        self.assertTrue(hasattr(settings, "FREEZE_FOLLOW_SITEMAP_URLS"))
        self.assertTrue(settings.FREEZE_FOLLOW_SITEMAP_URLS)

    def test_freeze_follow_html_urls_is_set(self):
        self.assertTrue(hasattr(settings, "FREEZE_FOLLOW_HTML_URLS"))
        self.assertTrue(settings.FREEZE_FOLLOW_HTML_URLS)

    def test_freeze_report_invalid_urls_is_set(self):
        self.assertTrue(hasattr(settings, "FREEZE_REPORT_INVALID_URLS"))
        self.assertFalse(settings.FREEZE_REPORT_INVALID_URLS)

    def test_freeze_report_invalid_urls_subject_is_set(self):
        self.assertTrue(hasattr(settings, "FREEZE_REPORT_INVALID_URLS_SUBJECT"))
        self.assertIsInstance(settings.FREEZE_REPORT_INVALID_URLS_SUBJECT, str)

    def test_freeze_include_media_is_set(self):
        self.assertTrue(hasattr(settings, "FREEZE_INCLUDE_MEDIA"))
        self.assertTrue(settings.FREEZE_INCLUDE_MEDIA)

    def test_freeze_include_static_is_set(self):
        self.assertTrue(hasattr(settings, "FREEZE_INCLUDE_STATIC"))
        self.assertTrue(settings.FREEZE_INCLUDE_STATIC)

    def test_freeze_zip_all_is_set(self):
        self.assertTrue(hasattr(settings, "FREEZE_ZIP_ALL"))
        self.assertFalse(settings.FREEZE_ZIP_ALL)

    def test_freeze_zip_name_has_zip_extension(self):
        self.assertTrue(hasattr(settings, "FREEZE_ZIP_NAME"))
        self.assertTrue(settings.FREEZE_ZIP_NAME.lower().endswith(".zip"))

    def test_freeze_zip_path_is_set(self):
        self.assertTrue(hasattr(settings, "FREEZE_ZIP_PATH"))
        self.assertTrue(os.path.isabs(settings.FREEZE_ZIP_PATH))
        self.assertTrue(settings.FREEZE_ZIP_PATH.lower().endswith(".zip"))

    def test_freeze_request_headers_is_set(self):
        self.assertTrue(hasattr(settings, "FREEZE_REQUEST_HEADERS"))
        self.assertIsInstance(settings.FREEZE_REQUEST_HEADERS, dict)
        self.assertIn("user-agent", settings.FREEZE_REQUEST_HEADERS)
