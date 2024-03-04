from django.contrib.sites.models import Site

from freeze import settings


def get_site_url():
    site_url = settings.FREEZE_SITE_URL
    if site_url is None:
        # handled this way to remove DB dependency unless strictly needed.
        # If FREEZE_SITE_URL is set then collectstatic can be called
        # without needing a db setup, which is useful for build servers
        protocol = settings.FREEZE_PROTOCOL
        domain = Site.objects.get_current().domain
        return f"{protocol}{domain}"
    return site_url
