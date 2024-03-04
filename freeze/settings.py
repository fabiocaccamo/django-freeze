import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

FREEZE_ROOT = getattr(
    settings,
    "FREEZE_ROOT",
    os.path.abspath(os.path.join(settings.MEDIA_ROOT, "../freeze/")),
)

if not os.path.isabs(FREEZE_ROOT):
    raise ImproperlyConfigured("settings.FREEZE_ROOT should be an absolute path")

media_root = settings.MEDIA_ROOT
static_root = settings.STATIC_ROOT
if (
    media_root
    and media_root.find(FREEZE_ROOT) == 0
    or static_root
    and static_root.find(FREEZE_ROOT) == 0
):
    raise ImproperlyConfigured(
        "settings.FREEZE_ROOT can't be a subdirectory of MEDIA_ROOT or STATIC_ROOT"
    )

FREEZE_MEDIA_ROOT = settings.MEDIA_ROOT
FREEZE_MEDIA_URL = settings.MEDIA_URL

if not FREEZE_MEDIA_ROOT:
    raise ImproperlyConfigured(
        "settings.FREEZE_MEDIA_ROOT can't be None, "
        "please configure settings.MEDIA_ROOT"
    )

if not FREEZE_MEDIA_URL:
    raise ImproperlyConfigured(
        "settings.FREEZE_MEDIA_URL can't be None, "
        "please configure settings.FREEZE_MEDIA_URL"
    )

FREEZE_STATIC_ROOT = settings.STATIC_ROOT
FREEZE_STATIC_URL = settings.STATIC_URL

if not FREEZE_STATIC_ROOT:
    raise ImproperlyConfigured(
        "settings.FREEZE_STATIC_ROOT can't be None, "
        "please configure settings.STATIC_ROOT"
    )

if not FREEZE_STATIC_URL:
    raise ImproperlyConfigured(
        "settings.FREEZE_STATIC_URL can't be None, "
        "please configure settings.STATIC_URL"
    )

FREEZE_USE_HTTPS = getattr(settings, "FREEZE_USE_HTTPS", False)
FREEZE_PROTOCOL = "https://" if FREEZE_USE_HTTPS else "http://"
FREEZE_SITE_URL = getattr(settings, "FREEZE_SITE_URL", None)

FREEZE_BASE_URL = getattr(settings, "FREEZE_BASE_URL", None)
if FREEZE_BASE_URL:
    if FREEZE_BASE_URL.startswith("/") or FREEZE_BASE_URL.startswith("http"):
        if not FREEZE_BASE_URL.endswith("/"):
            FREEZE_BASE_URL += "/"
    else:
        raise ImproperlyConfigured(
            "settings.FREEZE_BASE_URL should start with "
            "'/' or 'http' or be an empty string"
        )

FREEZE_RELATIVE_URLS = getattr(settings, "FREEZE_RELATIVE_URLS", False)
if FREEZE_RELATIVE_URLS and FREEZE_BASE_URL is not None:
    raise ImproperlyConfigured(
        "settings.FREEZE_RELATIVE_URLS can't be set "
        "to True if FREEZE_BASE_URL is specified"
    )

FREEZE_LOCAL_URLS = getattr(settings, "FREEZE_LOCAL_URLS", False)
if FREEZE_LOCAL_URLS and not FREEZE_RELATIVE_URLS:
    raise ImproperlyConfigured(
        "settings.FREEZE_LOCAL_URLS can't be set "
        "to True if FREEZE_RELATIVE_URLS is set to False"
    )

FREEZE_FOLLOW_SITEMAP_URLS = getattr(settings, "FREEZE_FOLLOW_SITEMAP_URLS", True)
FREEZE_FOLLOW_HTML_URLS = getattr(settings, "FREEZE_FOLLOW_HTML_URLS", True)

FREEZE_REPORT_INVALID_URLS = getattr(settings, "FREEZE_REPORT_INVALID_URLS", False)
FREEZE_REPORT_INVALID_URLS_SUBJECT = getattr(
    settings, "FREEZE_REPORT_INVALID_URLS_SUBJECT", "[freeze] invalid urls"
)

FREEZE_INCLUDE_MEDIA = getattr(settings, "FREEZE_INCLUDE_MEDIA", True)
FREEZE_INCLUDE_STATIC = getattr(settings, "FREEZE_INCLUDE_STATIC", True)

FREEZE_ZIP_ALL = getattr(settings, "FREEZE_ZIP_ALL", False)
FREEZE_ZIP_NAME = getattr(settings, "FREEZE_ZIP_NAME", "freeze")

if len(FREEZE_ZIP_NAME) >= 4 and FREEZE_ZIP_NAME[-4:].lower() != ".zip":
    FREEZE_ZIP_NAME += ".zip"

FREEZE_ZIP_PATH = os.path.abspath(os.path.join(FREEZE_ROOT, FREEZE_ZIP_NAME))

FREEZE_REQUEST_HEADERS = getattr(
    settings, "FREEZE_REQUEST_HEADERS", {"user-agent": "django-freeze"}
)
