# -*- coding: utf-8 -*-

from django.conf.urls import url

from freeze import views


urlpatterns = [
    url(r'^download-static-site/$', views.download_static_site, name='freeze_download_static_site'),
    url(r'^generate-static-site/$', views.generate_static_site, name='freeze_generate_static_site'),
]

