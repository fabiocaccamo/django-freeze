import os
import tempfile
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse


class ViewsTestCase(TestCase):
    """
    This class describes a views test case.
    """

    def setUp(self):
        self.staff_user = User.objects.create_user(
            username="staff",
            password="pass",
            is_staff=True,
            is_active=True,
        )
        self.regular_user = User.objects.create_user(
            username="user",
            password="pass",
            is_staff=False,
            is_active=True,
        )

    # -------------------------------------------------------------------------
    # generate_static_site
    # -------------------------------------------------------------------------

    @patch("freeze.views.writer.write")
    @patch("freeze.views.scanner.scan", return_value=[])
    def test_generate_static_site_staff_returns_200(self, mock_scan, mock_write):
        self.client.login(username="staff", password="pass")
        response = self.client.get(reverse("freeze_generate_static_site"))
        self.assertEqual(response.status_code, 200)
        mock_scan.assert_called_once()
        mock_write.assert_called_once()

    def test_generate_static_site_anonymous_raises_403(self):
        response = self.client.get(reverse("freeze_generate_static_site"))
        self.assertEqual(response.status_code, 403)

    def test_generate_static_site_non_staff_raises_403(self):
        self.client.login(username="user", password="pass")
        response = self.client.get(reverse("freeze_generate_static_site"))
        self.assertEqual(response.status_code, 403)

    @patch("freeze.views.writer.write", side_effect=OSError("disk full"))
    @patch("freeze.views.scanner.scan", return_value=[])
    def test_generate_static_site_os_error_returns_500(self, mock_scan, mock_write):
        self.client.login(username="staff", password="pass")
        response = self.client.get(reverse("freeze_generate_static_site"))
        self.assertEqual(response.status_code, 500)

    # -------------------------------------------------------------------------
    # download_static_site
    # -------------------------------------------------------------------------

    @patch("freeze.views.download_zip")
    @patch("freeze.views.writer.write")
    @patch("freeze.views.scanner.scan", return_value=[])
    def test_download_static_site_staff_returns_200(
        self, mock_scan, mock_write, mock_download
    ):
        from django.http import HttpResponse

        mock_download.return_value = HttpResponse(
            b"zipdata", content_type="application/zip"
        )
        self.client.login(username="staff", password="pass")
        response = self.client.get(reverse("freeze_download_static_site"))
        self.assertEqual(response.status_code, 200)
        mock_scan.assert_called_once()
        mock_write.assert_called_once()

    def test_download_static_site_anonymous_raises_403(self):
        response = self.client.get(reverse("freeze_download_static_site"))
        self.assertEqual(response.status_code, 403)

    def test_download_static_site_non_staff_raises_403(self):
        self.client.login(username="user", password="pass")
        response = self.client.get(reverse("freeze_download_static_site"))
        self.assertEqual(response.status_code, 403)

    @patch("freeze.views.writer.write", side_effect=Exception("unexpected"))
    @patch("freeze.views.scanner.scan", return_value=[])
    def test_download_static_site_exception_returns_500(self, mock_scan, mock_write):
        self.client.login(username="staff", password="pass")
        response = self.client.get(reverse("freeze_download_static_site"))
        self.assertEqual(response.status_code, 500)

    @patch("freeze.views.download_zip")
    @patch("freeze.views.writer.write")
    @patch("freeze.views.scanner.scan", return_value=[])
    def test_download_static_site_include_media_0(
        self, mock_scan, mock_write, mock_download
    ):
        from django.http import HttpResponse

        mock_download.return_value = HttpResponse(b"z", content_type="application/zip")
        self.client.login(username="staff", password="pass")
        self.client.get(reverse("freeze_download_static_site") + "?include_media=0")
        _, kwargs = mock_write.call_args
        self.assertFalse(kwargs.get("include_media", True))

    @patch("freeze.views.download_zip")
    @patch("freeze.views.writer.write")
    @patch("freeze.views.scanner.scan", return_value=[])
    def test_download_static_site_include_static_0(
        self, mock_scan, mock_write, mock_download
    ):
        from django.http import HttpResponse

        mock_download.return_value = HttpResponse(b"z", content_type="application/zip")
        self.client.login(username="staff", password="pass")
        self.client.get(reverse("freeze_download_static_site") + "?include_static=0")
        _, kwargs = mock_write.call_args
        self.assertFalse(kwargs.get("include_static", True))

    # -------------------------------------------------------------------------
    # download_zip
    # -------------------------------------------------------------------------

    def test_download_zip_returns_streaming_response(self):
        from freeze.views import download_zip

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
            tmp.write(b"PK fake zip content")
            tmp_path = tmp.name

        try:
            with override_settings(
                FREEZE_ZIP_PATH=tmp_path,
                FREEZE_ZIP_NAME="freeze.zip",
            ):
                response = download_zip(path=tmp_path, name="freeze.zip")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response["Content-Type"], "application/zip")
            self.assertIn("freeze.zip", response["Content-Disposition"])
        finally:
            os.unlink(tmp_path)
