import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

if not hasattr(settings, "FREEZE_ROOT"):
    settings.FREEZE_ROOT = os.path.abspath(
        os.path.join(settings.MEDIA_ROOT, "../freeze/")
    )

if not os.path.isabs(settings.FREEZE_ROOT):
    raise ImproperlyConfigured("settings.FREEZE_ROOT should be an absolute path")

media_root = settings.MEDIA_ROOT
static_root = settings.STATIC_ROOT
if (
    media_root
    and media_root.find(settings.FREEZE_ROOT) == 0
    or static_root
    and static_root.find(settings.FREEZE_ROOT) == 0
):
    raise ImproperlyConfigured(
        "settings.FREEZE_ROOT can't be a subdirectory of "
        "settings.MEDIA_ROOT or settings.STATIC_ROOT"
    )

if not hasattr(settings, "FREEZE_MEDIA_ROOT"):
    settings.FREEZE_MEDIA_ROOT = getattr(settings, "MEDIA_ROOT", None)

if not settings.FREEZE_MEDIA_ROOT:
    raise ImproperlyConfigured(
        "settings.FREEZE_MEDIA_ROOT can't be None, please configure settings.MEDIA_ROOT"
    )

if not hasattr(settings, "FREEZE_MEDIA_URL"):
    settings.FREEZE_MEDIA_URL = getattr(settings, "MEDIA_URL", None)

if not settings.FREEZE_MEDIA_URL:
    raise ImproperlyConfigured(
        "settings.FREEZE_MEDIA_URL can't be None, please configure settings.MEDIA_URL"
    )

if not hasattr(settings, "FREEZE_STATIC_ROOT"):
    settings.FREEZE_STATIC_ROOT = getattr(settings, "STATIC_ROOT", None)

if not settings.FREEZE_STATIC_ROOT:
    raise ImproperlyConfigured(
        "settings.FREEZE_STATIC_ROOT can't be None, "
        "please configure settings.STATIC_ROOT"
    )

if not hasattr(settings, "FREEZE_STATIC_URL"):
    settings.FREEZE_STATIC_URL = getattr(settings, "STATIC_URL", None)

if not settings.FREEZE_STATIC_URL:
    raise ImproperlyConfigured(
        "settings.FREEZE_STATIC_URL can't be None, please configure settings.STATIC_URL"
    )

if not hasattr(settings, "FREEZE_USE_HTTPS"):
    settings.FREEZE_USE_HTTPS = False if settings.DEBUG else True

if not hasattr(settings, "FREEZE_PROTOCOL"):
    settings.FREEZE_PROTOCOL = "https://" if settings.FREEZE_USE_HTTPS else "http://"

if not hasattr(settings, "FREEZE_SITE_URL"):
    settings.FREEZE_SITE_URL = None

if not hasattr(settings, "FREEZE_BASE_URL"):
    settings.FREEZE_BASE_URL = ""

if settings.FREEZE_BASE_URL:
    if settings.FREEZE_BASE_URL.startswith(("/", "http")):
        if not settings.FREEZE_BASE_URL.endswith("/"):
            settings.FREEZE_BASE_URL += "/"
    else:
        raise ImproperlyConfigured(
            "settings.FREEZE_BASE_URL should start with "
            "'/' or 'http' or be an empty string"
        )

if not hasattr(settings, "FREEZE_RELATIVE_URLS"):
    settings.FREEZE_RELATIVE_URLS = False

if settings.FREEZE_RELATIVE_URLS and settings.FREEZE_BASE_URL:
    raise ImproperlyConfigured(
        "settings.FREEZE_RELATIVE_URLS can't be set "
        "to True if settings.FREEZE_BASE_URL is specified"
    )

if not hasattr(settings, "FREEZE_LOCAL_URLS"):
    settings.FREEZE_LOCAL_URLS = False

if settings.FREEZE_LOCAL_URLS and not settings.FREEZE_RELATIVE_URLS:
    raise ImproperlyConfigured(
        "settings.FREEZE_LOCAL_URLS can't be set "
        "to True if settings.FREEZE_RELATIVE_URLS is set to False"
    )

if not hasattr(settings, "FREEZE_FOLLOW_SITEMAP_URLS"):
    settings.FREEZE_FOLLOW_SITEMAP_URLS = True

if not hasattr(settings, "FREEZE_FOLLOW_HTML_URLS"):
    settings.FREEZE_FOLLOW_HTML_URLS = True

if not hasattr(settings, "FREEZE_REPORT_INVALID_URLS"):
    settings.FREEZE_REPORT_INVALID_URLS = False

if not hasattr(settings, "FREEZE_REPORT_INVALID_URLS_SUBJECT"):
    settings.FREEZE_REPORT_INVALID_URLS_SUBJECT = "[freeze] invalid urls"

if not hasattr(settings, "FREEZE_INCLUDE_MEDIA"):
    settings.FREEZE_INCLUDE_MEDIA = True

if not hasattr(settings, "FREEZE_INCLUDE_STATIC"):
    settings.FREEZE_INCLUDE_STATIC = True

if not hasattr(settings, "FREEZE_ZIP_ALL"):
    settings.FREEZE_ZIP_ALL = False

if not hasattr(settings, "FREEZE_ZIP_NAME"):
    settings.FREEZE_ZIP_NAME = "freeze"

if (
    len(settings.FREEZE_ZIP_NAME) >= 4
    and settings.FREEZE_ZIP_NAME[-4:].lower() != ".zip"
):
    settings.FREEZE_ZIP_NAME += ".zip"

if not hasattr(settings, "FREEZE_ZIP_PATH"):
    settings.FREEZE_ZIP_PATH = os.path.abspath(
        os.path.join(settings.FREEZE_ROOT, settings.FREEZE_ZIP_NAME)
    )

if not hasattr(settings, "FREEZE_REQUEST_HEADERS"):
    settings.FREEZE_REQUEST_HEADERS = {
        "user-agent": "django-freeze",
    }
