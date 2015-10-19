# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^generate-static-site/$', 'freeze.views.generate_static_site', name='freeze_generate_static_site'), 
)

