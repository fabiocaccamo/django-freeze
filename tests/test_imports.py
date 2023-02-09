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

        self.assertTrue(isinstance(__author__, str))
        self.assertTrue(isinstance(__copyright__, str))
        self.assertTrue(isinstance(__description__, str))
        self.assertTrue(isinstance(__email__, str))
        self.assertTrue(isinstance(__license__, str))
        self.assertTrue(isinstance(__title__, str))
        self.assertTrue(isinstance(__version__, str))

    def test_imports_from_parser(self):
        from freeze.parser import parse_html_urls, parse_sitemap_urls, replace_base_url

        self.assertTrue(callable(parse_html_urls))
        self.assertTrue(callable(parse_sitemap_urls))
        self.assertTrue(callable(replace_base_url))

    def test_imports_from_scanner(self):
        from freeze.scanner import scan

        self.assertTrue(callable(scan))

    def test_imports_from_views(self):
        from freeze.views import download_static_site, generate_static_site

        self.assertTrue(callable(download_static_site))
        self.assertTrue(callable(generate_static_site))

    def test_imports_from_writer(self):
        from freeze.writer import write

        self.assertTrue(callable(write))
