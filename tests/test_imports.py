# -*- coding: utf-8 -*-

from django.urls import reverse
from django.test import TestCase


class ImportsTestCase(TestCase):
    """
    This class describes an imports test case.
    """

    def test_imports_from_metadata(self):
        from freeze.metadata import (
            __author__,
            __copyright__,
            __description__,
            __email__,
            __license__,
            __title__,
            __version__,
        )

    def test_imports_from_parser(self):
        from freeze.parser import (
            parse_sitemap_urls,
            parse_html_urls,
            replace_base_url,
        )

    def test_imports_from_scanner(self):
        from freeze.scanner import (
            scan,
        )

    def test_imports_from_views(self):
        from freeze.views import (
            download_static_site,
            generate_static_site,
        )

    def test_imports_from_writer(self):
        from freeze.writer import (
            write,
        )
