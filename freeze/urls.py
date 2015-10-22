# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^download-static-site/$', 'freeze.views.download_static_site', name='freeze_download_static_site'), 
    url(r'^generate-static-site/$', 'freeze.views.generate_static_site', name='freeze_generate_static_site'), 
)

