# -*- coding: utf-8 -*-

if django.VERSION < (2, 0):
    from django.conf.urls import url as re_path
else:
    from django.urls import re_path

from freeze import views


urlpatterns = [
    re_path(r'^download-static-site/$', views.download_static_site, name='freeze_download_static_site'),
    re_path(r'^generate-static-site/$', views.generate_static_site, name='freeze_generate_static_site'),
]
