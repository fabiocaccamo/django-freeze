from django.test import TestCase, override_settings

from freeze.sites import get_site_url


class SitesTestCase(TestCase):
    """
    This class describes a sites test case.
    """

    @override_settings(
        FREEZE_SITE_URL="https://django-freeze.com",
    )
    def test_get_site_url_with_setting_defined(self):
        site_url = get_site_url()
        self.assertEqual(site_url, "https://django-freeze.com")

    def test_get_site_url_without_setting_defined(self):
        site_url = get_site_url()
        self.assertEqual(site_url, "https://example.com")
