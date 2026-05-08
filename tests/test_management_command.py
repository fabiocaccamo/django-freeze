import tempfile
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase, override_settings


class GenerateStaticSiteCommandTestCase(TestCase):
    """
    This class describes a management command test case for generate_static_site.
    """

    @patch("freeze.management.commands.generate_static_site.writer.write")
    @patch(
        "freeze.management.commands.generate_static_site.scanner.scan",
        return_value=[],
    )
    def test_command_calls_scan_and_write(self, mock_scan, mock_write):
        with tempfile.TemporaryDirectory() as freeze_root:
            with override_settings(
                FREEZE_ZIP_ALL=False,
                FREEZE_ROOT=freeze_root,
            ):
                call_command("generate_static_site")

        mock_scan.assert_called_once()
        mock_write.assert_called_once()

    @patch("freeze.management.commands.generate_static_site.writer.write")
    @patch(
        "freeze.management.commands.generate_static_site.scanner.scan",
        return_value=[],
    )
    def test_command_passes_zip_all_from_settings(self, mock_scan, mock_write):
        with tempfile.TemporaryDirectory() as freeze_root:
            with override_settings(
                FREEZE_ZIP_ALL=True,
                FREEZE_ROOT=freeze_root,
            ):
                call_command("generate_static_site")

        _args, kwargs = mock_write.call_args
        self.assertTrue(kwargs.get("zip_all", False))
        self.assertTrue(kwargs.get("html_in_memory", False))

    @patch("freeze.management.commands.generate_static_site.writer.write")
    @patch(
        "freeze.management.commands.generate_static_site.scanner.scan",
        return_value=[],
    )
    def test_command_zip_in_memory_is_false(self, mock_scan, mock_write):
        with tempfile.TemporaryDirectory() as freeze_root:
            with override_settings(
                FREEZE_ZIP_ALL=False,
                FREEZE_ROOT=freeze_root,
            ):
                call_command("generate_static_site")

        _args, kwargs = mock_write.call_args
        self.assertFalse(kwargs.get("zip_in_memory", True))
