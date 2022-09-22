# -*- coding: utf-8 -*-

if django.VERSION < (2, 0):
    from django.conf.urls import include, url as path
else:
    from django.urls import include, path

from freeze import views


urlpatterns = [
    path("download-static-site/", views.download_static_site, name="freeze_download_static_site"),
    path("generate-static-site/", views.generate_static_site, name="freeze_generate_static_site"),
]
