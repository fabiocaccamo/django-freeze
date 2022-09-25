# -*- coding: utf-8 -*-

from django.test import TestCase


class MetadataTestCase(TestCase):
    """
    This class describes a metadata test case.
    """

    def test_metadata(self):
        from freeze.metadata import (
            __author__,
            __copyright__,
            __description__,
            __email__,
            __license__,
            __title__,
            __version__,
        )
