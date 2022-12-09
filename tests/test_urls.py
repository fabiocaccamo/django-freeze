from django.test import TestCase
from django.urls import reverse


class UrlsTestCase(TestCase):
    """
    This class describes an urls test case.
    """

    def test_urls(self):
        download_static_site_url = reverse("freeze_download_static_site")
        self.assertEqual(download_static_site_url, "/download-static-site/")
        generate_static_site_url = reverse("freeze_generate_static_site")
        self.assertEqual(generate_static_site_url, "/generate-static-site/")
