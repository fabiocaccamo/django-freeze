# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured

import os


FREEZE_ROOT = getattr(settings, 'FREEZE_ROOT', os.path.abspath(os.path.join(settings.MEDIA_ROOT, '../freeze/')) )

if not os.path.isabs(FREEZE_ROOT):
    raise ImproperlyConfigured('settings.FREEZE_ROOT should be an absolute path')

if settings.MEDIA_ROOT.find(FREEZE_ROOT) == 0 or settings.STATIC_ROOT.find(FREEZE_ROOT) == 0:
    raise ImproperlyConfigured('settings.FREEZE_ROOT cannot be a subdirectory of MEDIA_ROOT or STATIC_ROOT')

FREEZE_HTML_ROOT = os.path.abspath(os.path.normpath(settings.FREEZE_ROOT + '/html/'))

FREEZE_MEDIA_ROOT = settings.MEDIA_ROOT
FREEZE_MEDIA_URL = settings.MEDIA_URL

FREEZE_STATIC_ROOT = settings.STATIC_ROOT
FREEZE_STATIC_URL = settings.STATIC_URL


FREEZE_USE_HTTPS = getattr(settings, 'FREEZE_USE_HTTPS', False)
FREEZE_SITE = Site.objects.get_current()
FREEZE_PROTOCOL = 'https://' if FREEZE_USE_HTTPS else 'http://'
FREEZE_DOMAIN = FREEZE_SITE.domain
FREEZE_HOST = FREEZE_PROTOCOL + FREEZE_DOMAIN

FREEZE_SITEMAP_MODE = getattr(settings, 'FREEZE_SITEMAP_MODE', True)
FREEZE_FOLLOW_MODE = getattr(settings, 'FREEZE_FOLLOW_MODE', False)

FREEZE_REPORT_INVALID_URLS = getattr(settings, 'FREEZE_REPORT_INVALID_URLS', False)
FREEZE_REPORT_INVALID_URLS_SUBJECT = getattr(settings, 'FREEZE_REPORT_INVALID_URLS_SUBJECT', '[freeze] invalid urls')


FREEZE_ZIP_NAME = getattr(settings, 'FREEZE_ZIP_NAME', 'freeze')

if len(FREEZE_ZIP_NAME) >= 4 and FREEZE_ZIP_NAME[-4:].lower() != '.zip':
    FREEZE_ZIP_NAME += '.zip'
    
FREEZE_ZIP_NAME_WITH_PREFIX = '%s' + FREEZE_ZIP_NAME


FREEZE_ZIP_PATH = os.path.abspath(os.path.join(FREEZE_ROOT, FREEZE_ZIP_NAME))

FREEZE_ZIP_INCLUDE_MEDIA = getattr(settings, 'FREEZE_ZIP_INCLUDE_MEDIA', True)
FREEZE_ZIP_INCLUDE_STATIC = getattr(settings, 'FREEZE_ZIP_INCLUDE_STATIC', True)
FREEZE_ZIP_INCLUDE_STATIC_APPS = getattr(settings, 'FREEZE_ZIP_INCLUDE_STATIC_APPS', ())

if FREEZE_ZIP_INCLUDE_STATIC_APPS:
    
    for app_name in FREEZE_ZIP_INCLUDE_STATIC_APPS:
        
        if not app_name in settings.INSTALLED_APPS:
            raise ImproperlyConfigured('%s not founded in settings.INSTALLED_APPS' % (app_name, ))
            
            