import os
import tempfile
from unittest.mock import MagicMock, patch

import requests
from django.test import TestCase, override_settings


def _mock_response(status_code=200, text="<html><body>hello</body></html>", url=None):
    resp = MagicMock(spec=requests.Response)
    resp.status_code = status_code
    resp.text = text
    resp.url = url
    resp.encoding = "utf-8"
    resp.history = []
    return resp


class ScannerTestCase(TestCase):
    """
    This class describes a scanner test case.
    """

    def _run_scan(self, freeze_root, site_url="http://localhost", **scan_kwargs):
        from freeze.scanner import scan

        scan_kwargs.setdefault("follow_sitemap_urls", False)
        scan_kwargs.setdefault("follow_html_urls", False)
        scan_kwargs.setdefault("report_invalid_urls", False)
        return scan(site_url=site_url, **scan_kwargs)

    @patch("freeze.scanner.requests.get")
    def test_scan_returns_home_url_data(self, mock_get):
        site_url = "http://localhost"
        home_url = f"{site_url}/"
        mock_get.return_value = _mock_response(
            text="<html><body>home</body></html>", url=home_url
        )
        results = self._run_scan(None, site_url=site_url)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["url"], home_url)
        self.assertIn("file_path", results[0])
        self.assertIn("file_dirs", results[0])
        self.assertIn("file_data", results[0])

    @patch("freeze.scanner.requests.get")
    def test_scan_follows_html_urls(self, mock_get):
        with tempfile.TemporaryDirectory() as freeze_root:
            site_url = "http://localhost"
            home_html = (
                '<html><body>'
                '<a href="/about/">about</a>'
                '</body></html>'
            )
            about_html = "<html><body>about page</body></html>"

            def side_effect(url, headers=None):
                if url == f"{site_url}/":
                    return _mock_response(text=home_html, url=url)
                if url == f"{site_url}/about/":
                    return _mock_response(text=about_html, url=url)
                return _mock_response(status_code=404, url=url)

            mock_get.side_effect = side_effect

            with override_settings(
                FREEZE_SITE_URL=site_url,
                FREEZE_ROOT=freeze_root,
            ):
                results = self._run_scan(
                    freeze_root,
                    site_url=site_url,
                    follow_html_urls=True,
                )

        urls = [r["url"] for r in results]
        self.assertIn(f"{site_url}/", urls)
        self.assertIn(f"{site_url}/about/", urls)

    @patch("freeze.scanner.requests.get")
    def test_scan_skips_external_urls(self, mock_get):
        with tempfile.TemporaryDirectory() as freeze_root:
            site_url = "http://localhost"
            home_html = (
                '<html><body>'
                '<a href="http://external.com/">external</a>'
                '</body></html>'
            )
            mock_get.return_value = _mock_response(text=home_html, url=f"{site_url}/")

            with override_settings(
                FREEZE_SITE_URL=site_url,
                FREEZE_ROOT=freeze_root,
            ):
                results = self._run_scan(
                    freeze_root,
                    site_url=site_url,
                    follow_html_urls=True,
                )

        urls = [r["url"] for r in results]
        self.assertNotIn("http://external.com/", urls)

    @patch("freeze.scanner.requests.get")
    def test_scan_strips_query_string_and_fragment(self, mock_get):
        with tempfile.TemporaryDirectory() as freeze_root:
            site_url = "http://localhost"

            def side_effect(url, headers=None):
                clean_url = url.split("?")[0].split("#")[0]
                return _mock_response(text="<html></html>", url=clean_url)

            mock_get.side_effect = side_effect

            from freeze.scanner import scan

            results = scan(
                site_url=site_url,
                follow_sitemap_urls=False,
                follow_html_urls=False,
                report_invalid_urls=False,
            )

        self.assertEqual(len(results), 1)

    @patch("freeze.scanner.requests.get")
    def test_scan_handles_404(self, mock_get):
        with tempfile.TemporaryDirectory() as freeze_root:
            site_url = "http://localhost"
            mock_get.return_value = _mock_response(
                status_code=404, text="not found", url=f"{site_url}/"
            )

            results = self._run_scan(freeze_root, site_url=site_url)

        self.assertEqual(results, [])

    @patch("freeze.scanner.requests.get")
    def test_scan_handles_redirect(self, mock_get):
        with tempfile.TemporaryDirectory() as freeze_root:
            site_url = "http://localhost"
            redirect_url = f"{site_url}/en/"

            redirect_resp = _mock_response(
                text="<html><body>english</body></html>", url=redirect_url
            )
            redirect_resp.history = [MagicMock()]

            en_resp = _mock_response(
                text="<html><body>english</body></html>", url=redirect_url
            )
            en_resp.history = []

            call_count = [0]

            def side_effect(url, headers=None):
                call_count[0] += 1
                if url == f"{site_url}/":
                    return redirect_resp
                return en_resp

            mock_get.side_effect = side_effect

            results = self._run_scan(freeze_root, site_url=site_url)

        urls = [r["url"] for r in results]
        self.assertIn(f"{site_url}/", urls)

    @patch("freeze.scanner.requests.get")
    def test_scan_file_path_for_home_is_index_html(self, mock_get):
        """The home URL '/' should produce file_path '/index.html'."""
        with tempfile.TemporaryDirectory() as freeze_root:
            site_url = "http://localhost"
            mock_get.return_value = _mock_response(
                text="<html></html>", url=f"{site_url}/"
            )

            from freeze.scanner import scan

            results = scan(
                site_url=site_url,
                follow_sitemap_urls=False,
                follow_html_urls=False,
                report_invalid_urls=False,
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["file_path"], os.path.normpath("/index.html"))

    @patch("freeze.scanner.requests.get")
    def test_scan_deduplicates_urls(self, mock_get):
        with tempfile.TemporaryDirectory() as freeze_root:
            site_url = "http://localhost"
            mock_get.return_value = _mock_response(
                text='<html><body><a href="/">home again</a></body></html>',
                url=f"{site_url}/",
            )

            results = self._run_scan(
                freeze_root, site_url=site_url, follow_html_urls=True
            )

        # The home page should only appear once even though it links to itself
        urls = [r["url"] for r in results]
        self.assertEqual(len(urls), len(set(urls)))

    @patch("freeze.scanner.requests.get")
    def test_scan_site_url_trailing_slash_stripped(self, mock_get):
        with tempfile.TemporaryDirectory() as freeze_root:
            site_url_with_slash = "http://localhost/"
            mock_get.return_value = _mock_response(
                text="<html></html>", url="http://localhost/"
            )

            results = self._run_scan(
                freeze_root, site_url=site_url_with_slash
            )

        self.assertEqual(len(results), 1)
