# -*- coding: utf-8 -*-

import django

if django.VERSION < (2, 0):
    try:
        from django.conf.urls import url as re_path
    except ImportError:
        from django.core.urlresolvers import url as re_path
else:
    from django.urls import re_path

from freeze.views import download_static_site, generate_static_site


urlpatterns = [
    re_path(
        r"^download-static-site/$",
        download_static_site,
        name="freeze_download_static_site",
    ),
    re_path(
        r"^generate-static-site/$",
        generate_static_site,
        name="freeze_generate_static_site",
    ),
]
