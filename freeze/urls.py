# -*- coding: utf-8 -*-

from django.urls import path
from freeze import views

urlpatterns = [
    path(
        "download-static-site/",
        views.download_static_site,
        name="freeze_download_static_site",
    ),
    path(
        "generate-static-site/",
        views.generate_static_site,
        name="freeze_generate_static_site",
    ),
]
