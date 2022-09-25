# -*- coding: utf-8 -*-

import django

if django.VERSION < (2, 0):
    try:
        from django.conf.urls import reverse
    except ImportError:
        from django.core.urlresolvers import reverse
else:
    from django.urls import reverse

from django.test import TestCase


class UrlsTestCase(TestCase):
    """
    This class describes a metadata test case.
    """

    def test_urls(self):
        download_static_site_url = reverse("freeze_download_static_site")
        self.assertEqual(download_static_site_url, "/download-static-site/")
        generate_static_site_url = reverse("freeze_generate_static_site")
        self.assertEqual(generate_static_site_url, "/generate-static-site/")
