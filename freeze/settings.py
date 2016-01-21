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

FREEZE_MEDIA_ROOT = settings.MEDIA_ROOT
FREEZE_MEDIA_URL = settings.MEDIA_URL

FREEZE_STATIC_ROOT = settings.STATIC_ROOT
FREEZE_STATIC_URL = settings.STATIC_URL

FREEZE_USE_HTTPS = getattr(settings, 'FREEZE_USE_HTTPS', False)
FREEZE_SITE = Site.objects.get_current()
FREEZE_PROTOCOL = 'https://' if FREEZE_USE_HTTPS else 'http://'
FREEZE_DOMAIN = FREEZE_SITE.domain
FREEZE_SITE_URL = getattr(settings, 'FREEZE_SITE_URL', '%s%s' % (FREEZE_PROTOCOL, FREEZE_DOMAIN, ))

FREEZE_BASE_URL = getattr(settings, 'FREEZE_BASE_URL', None)

if FREEZE_BASE_URL:
    
    if FREEZE_BASE_URL.startswith('/') or FREEZE_BASE_URL.startswith('http'):
        
        if not FREEZE_BASE_URL.endswith('/'):
            FREEZE_BASE_URL += '/'
    else:
        raise ImproperlyConfigured('settings.FREEZE_BASE_URL should start with \'/\' or \'http\' or be an empty string')
    
FREEZE_RELATIVE_URLS = getattr(settings, 'FREEZE_RELATIVE_URLS', False)

if FREEZE_RELATIVE_URLS and FREEZE_BASE_URL != None:
    raise ImproperlyConfigured('settings.FREEZE_RELATIVE_URLS cannot be set to True if FREEZE_BASE_URL is specified')
    
FREEZE_LOCAL_URLS = getattr(settings, 'FREEZE_LOCAL_URLS', False)

if FREEZE_LOCAL_URLS and not FREEZE_RELATIVE_URLS:
    raise ImproperlyConfigured('settings.FREEZE_LOCAL_URLS cannot be set to True if FREEZE_RELATIVE_URLS is set to False')

FREEZE_FOLLOW_SITEMAP_URLS = getattr(settings, 'FREEZE_FOLLOW_SITEMAP_URLS', True)
FREEZE_FOLLOW_HTML_URLS = getattr(settings, 'FREEZE_FOLLOW_HTML_URLS', True)

FREEZE_REPORT_INVALID_URLS = getattr(settings, 'FREEZE_REPORT_INVALID_URLS', False)
FREEZE_REPORT_INVALID_URLS_SUBJECT = getattr(settings, 'FREEZE_REPORT_INVALID_URLS_SUBJECT', '[freeze] invalid urls')

FREEZE_INCLUDE_MEDIA = getattr(settings, 'FREEZE_INCLUDE_MEDIA', True)
FREEZE_INCLUDE_STATIC = getattr(settings, 'FREEZE_INCLUDE_STATIC', True)

FREEZE_ZIP_ALL = getattr(settings, 'FREEZE_ZIP_ALL', False)
FREEZE_ZIP_NAME = getattr(settings, 'FREEZE_ZIP_NAME', 'freeze')

if len(FREEZE_ZIP_NAME) >= 4 and FREEZE_ZIP_NAME[-4:].lower() != '.zip':
    FREEZE_ZIP_NAME += '.zip'

FREEZE_ZIP_PATH = os.path.abspath(os.path.join(FREEZE_ROOT, FREEZE_ZIP_NAME))

