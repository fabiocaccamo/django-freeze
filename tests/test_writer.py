import io
import os
import tempfile
import zipfile

from django.conf import settings
from django.test import TestCase, override_settings

from freeze.writer import write


class WriterTestCase(TestCase):
    """
    This class describes a writer test case.
    """

    def _make_data(self, entries):
        """Build the url data list expected by write()."""
        return [
            {
                "url": e["url"],
                "file_dirs": e["file_dirs"],
                "file_path": e["file_path"],
                "file_data": e["file_data"],
            }
            for e in entries
        ]

    def test_write_html_files_to_disk(self):
        with tempfile.TemporaryDirectory() as freeze_root:
            data = self._make_data(
                [
                    {
                        "url": "http://localhost/",
                        "file_dirs": "/",
                        "file_path": "/index.html",
                        "file_data": "<html><body>home</body></html>",
                    },
                    {
                        "url": "http://localhost/about/",
                        "file_dirs": "/about",
                        "file_path": "/about/index.html",
                        "file_data": "<html><body>about</body></html>",
                    },
                ]
            )
            with override_settings(
                FREEZE_ROOT=freeze_root,
                FREEZE_ZIP_ALL=False,
                FREEZE_INCLUDE_MEDIA=False,
                FREEZE_INCLUDE_STATIC=False,
                FREEZE_ZIP_PATH=os.path.join(freeze_root, "freeze.zip"),
            ):
                write(data, include_media=False, include_static=False, zip_all=False)

            index_path = os.path.join(freeze_root, "index.html")
            about_path = os.path.join(freeze_root, "about", "index.html")

            self.assertTrue(os.path.isfile(index_path))
            self.assertTrue(os.path.isfile(about_path))

            with open(index_path) as f:
                self.assertIn("home", f.read())
            with open(about_path) as f:
                self.assertIn("about", f.read())

    def test_write_zip_file(self):
        with tempfile.TemporaryDirectory() as freeze_root:
            zip_path = os.path.join(freeze_root, "freeze.zip")
            data = self._make_data(
                [
                    {
                        "url": "http://localhost/",
                        "file_dirs": "/",
                        "file_path": "/index.html",
                        "file_data": "<html><body>home</body></html>",
                    },
                ]
            )
            with override_settings(
                FREEZE_ROOT=freeze_root,
                FREEZE_ZIP_ALL=True,
                FREEZE_INCLUDE_MEDIA=False,
                FREEZE_INCLUDE_STATIC=False,
                FREEZE_ZIP_PATH=zip_path,
            ):
                write(
                    data,
                    include_media=False,
                    include_static=False,
                    zip_all=True,
                    zip_in_memory=False,
                )

            self.assertTrue(os.path.isfile(zip_path))
            with zipfile.ZipFile(zip_path) as zf:
                names = zf.namelist()
            self.assertTrue(any("index.html" in n for n in names))

    def test_write_zip_in_memory(self):
        with tempfile.TemporaryDirectory() as freeze_root:
            zip_path = os.path.join(freeze_root, "freeze.zip")
            data = self._make_data(
                [
                    {
                        "url": "http://localhost/",
                        "file_dirs": "/",
                        "file_path": "/index.html",
                        "file_data": "<html><body>home</body></html>",
                    },
                ]
            )
            with override_settings(
                FREEZE_ROOT=freeze_root,
                FREEZE_ZIP_ALL=True,
                FREEZE_INCLUDE_MEDIA=False,
                FREEZE_INCLUDE_STATIC=False,
                FREEZE_ZIP_PATH=zip_path,
            ):
                result = write(
                    data,
                    include_media=False,
                    include_static=False,
                    zip_all=True,
                    zip_in_memory=True,
                )

            self.assertIsNotNone(result)
            self.assertIsInstance(result, bytes)

            with zipfile.ZipFile(io.BytesIO(result)) as zf:
                names = zf.namelist()
            self.assertTrue(any("index.html" in n for n in names))

    def test_write_overwrites_existing_freeze_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            freeze_root = os.path.join(tmp, "freeze")
            os.makedirs(freeze_root)
            # Create a stale file that should be removed
            stale_file = os.path.join(freeze_root, "stale.html")
            with open(stale_file, "w") as f:
                f.write("stale")

            data = self._make_data(
                [
                    {
                        "url": "http://localhost/",
                        "file_dirs": "/",
                        "file_path": "/index.html",
                        "file_data": "<html>fresh</html>",
                    },
                ]
            )
            with override_settings(
                FREEZE_ROOT=freeze_root,
                FREEZE_ZIP_ALL=False,
                FREEZE_INCLUDE_MEDIA=False,
                FREEZE_INCLUDE_STATIC=False,
                FREEZE_ZIP_PATH=os.path.join(freeze_root, "freeze.zip"),
            ):
                write(data, include_media=False, include_static=False, zip_all=False)

            self.assertFalse(os.path.isfile(stale_file))
            self.assertTrue(os.path.isfile(os.path.join(freeze_root, "index.html")))

    def test_write_include_static(self):
        with tempfile.TemporaryDirectory() as tmp:
            freeze_root = os.path.join(tmp, "freeze")
            static_root = os.path.join(tmp, "static") + "/"
            os.makedirs(static_root)
            # Place a dummy static file
            with open(os.path.join(static_root, "app.css"), "w") as f:
                f.write("body {}")

            data = self._make_data(
                [
                    {
                        "url": "http://localhost/",
                        "file_dirs": "/",
                        "file_path": "/index.html",
                        "file_data": "<html></html>",
                    },
                ]
            )
            with override_settings(
                FREEZE_ROOT=freeze_root,
                FREEZE_STATIC_ROOT=static_root,
                FREEZE_ZIP_ALL=False,
                FREEZE_INCLUDE_MEDIA=False,
                FREEZE_INCLUDE_STATIC=True,
                FREEZE_ZIP_PATH=os.path.join(freeze_root, "freeze.zip"),
            ):
                write(data, include_media=False, include_static=True, zip_all=False)

            self.assertTrue(
                os.path.isfile(os.path.join(freeze_root, "app.css"))
            )

    def test_write_include_media(self):
        with tempfile.TemporaryDirectory() as tmp:
            freeze_root = os.path.join(tmp, "freeze")
            media_root = os.path.join(tmp, "media") + "/"
            os.makedirs(media_root)
            with open(os.path.join(media_root, "photo.jpg"), "w") as f:
                f.write("fake image")

            data = self._make_data(
                [
                    {
                        "url": "http://localhost/",
                        "file_dirs": "/",
                        "file_path": "/index.html",
                        "file_data": "<html></html>",
                    },
                ]
            )
            with override_settings(
                FREEZE_ROOT=freeze_root,
                FREEZE_MEDIA_ROOT=media_root,
                FREEZE_MEDIA_URL="/media/",
                FREEZE_ZIP_ALL=False,
                FREEZE_INCLUDE_MEDIA=True,
                FREEZE_INCLUDE_STATIC=False,
                FREEZE_ZIP_PATH=os.path.join(freeze_root, "freeze.zip"),
            ):
                write(data, include_media=True, include_static=False, zip_all=False)

            self.assertTrue(
                os.path.isfile(os.path.join(freeze_root, "media", "photo.jpg"))
            )

    def test_write_with_bytes_file_data(self):
        with tempfile.TemporaryDirectory() as freeze_root:
            data = self._make_data(
                [
                    {
                        "url": "http://localhost/",
                        "file_dirs": "/",
                        "file_path": "/index.html",
                        "file_data": b"<html><body>bytes</body></html>",
                    },
                ]
            )
            with override_settings(
                FREEZE_ROOT=freeze_root,
                FREEZE_ZIP_ALL=False,
                FREEZE_INCLUDE_MEDIA=False,
                FREEZE_INCLUDE_STATIC=False,
                FREEZE_ZIP_PATH=os.path.join(freeze_root, "freeze.zip"),
            ):
                write(data, include_media=False, include_static=False, zip_all=False)

            index_path = os.path.join(freeze_root, "index.html")
            self.assertTrue(os.path.isfile(index_path))
            with open(index_path) as f:
                self.assertIn("bytes", f.read())
