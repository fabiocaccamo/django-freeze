import logging
import os
import re

import requests
import xmltodict
from bs4 import BeautifulSoup
from django.conf import settings
from django.urls import NoReverseMatch, reverse

from freeze.sites import get_site_url

logger = logging.getLogger(__name__)


def parse_sitemap_urls(
    site_url=settings.FREEZE_SITE_URL,
    request_headers=settings.FREEZE_REQUEST_HEADERS,
):
    if site_url is None:
        site_url = get_site_url()

    urls = []

    # reverse sitemap url
    sitemap_ok = False
    sitemap_url = None

    try:
        sitemap_view_name = "django.contrib.sitemaps.views.sitemap"
        sitemap_url = reverse(sitemap_view_name)
    except NoReverseMatch:
        try:
            sitemap_url = reverse("sitemap")
        except NoReverseMatch as error:
            # sitemap_url = "/sitemap.xml"
            raise NoReverseMatch(
                f"Reverse for {sitemap_view_name!r} or 'sitemap' not found."
            ) from error

    # load sitemap
    sitemap_url = f"{site_url}{sitemap_url}"
    sitemap_request = requests.get(sitemap_url, headers=request_headers)
    sitemap_request.encoding = "utf-8"

    if sitemap_request.status_code == requests.codes.ok:
        try:
            sitemap_data = xmltodict.parse(sitemap_request.text)
            sitemap_ok = True
        except Exception:
            logger.info("sitemap parsing error...")
    else:
        logger.info("sitemap not found...")

    if sitemap_ok:
        sitemap_urls_data = sitemap_data.get("urlset", {}).get("url", {})

        # this happens if the sitemap only has a single entry
        if "loc" in sitemap_urls_data:
            sitemap_urls_data = [sitemap_urls_data]

        for sitemap_url_data in sitemap_urls_data:
            url = sitemap_url_data.get("loc", "")
            urls.append(url)

        urls = list(set(urls))
        urls.sort()

    return urls


def parse_html_urls(
    html,
    site_url=settings.FREEZE_SITE_URL,
    base_url="/",
    media_urls=False,
    static_urls=False,
    external_urls=False,
):
    if site_url is None:
        site_url = get_site_url()

    urls = []
    soup = BeautifulSoup(html, "html5lib")

    for url_node in soup.findAll("a"):
        url = url_node.get("href")

        if url:
            url = url.replace(site_url, "")

            if url.find(settings.FREEZE_MEDIA_URL) == 0 and not media_urls:
                # skip media files urls
                continue
            elif url.find(settings.FREEZE_STATIC_URL) == 0 and not static_urls:
                # skip static files urls
                continue
            elif url[0] == "#":
                # skip anchors
                continue
            elif url[0] == "/":
                # url already start from the site root
                url = f"{site_url}{url}"
                urls.append(url)
                continue
            elif ":" in url:
                # probably an external link or a link like
                # tel: mailto: skype: call: etc...
                if external_urls and url.lower().find("http") == 0:
                    urls.append(url)
                else:
                    continue
            else:
                # since it's a relative url let's merge it with the current page path
                url = os.path.normpath(
                    os.path.abspath(os.path.normpath(f"{base_url}/{url}"))
                )
                url = f"{site_url}{url}"
                urls.append(url)

    urls = list(set(urls))
    urls.sort()
    return urls


def replace_base_url_on_media_and_static_urls(text, base_url):
    # static and media urls should start with "/"
    media_url = settings.FREEZE_MEDIA_URL
    static_url = settings.FREEZE_STATIC_URL
    for url in (media_url, static_url):
        if url.startswith("/"):
            # fix media double slashes mistake
            text = text.replace(f"/{url}", url)
            # replace base url for urls outside quotes
            text = re.sub(
                r"([^\"\'\-\_\w\d])" + url,
                r"\1" + base_url + url[1:],
                text,
            )
    return text


def replace_base_url_on_urls_relative_to_root(text, base_url):
    # replace base url for all urls relative to root between "" or ''
    def sub_base_url(match_obj):
        startquote = match_obj.group(1)
        url = match_obj.group(4) or ""
        endquote = match_obj.group(6)
        return f"{startquote}{base_url}{url}{endquote}"

    text = re.sub(r"(\")((\/)([^\/](\\\"|(?!\").)*)?)(\")", sub_base_url, text)
    text = re.sub(r"(\')((\/)([^\/](\\\'|(?!\').)*)?)(\')", sub_base_url, text)
    return text


def replace_base_url(text, base_url):
    if base_url is None:
        return text

    text = replace_base_url_on_media_and_static_urls(
        text=text,
        base_url=base_url,
    )

    text = replace_base_url_on_urls_relative_to_root(
        text=text,
        base_url=base_url,
    )

    # replace base url in case of
    # <meta http-equiv="refresh" content="0; url=/en/" />
    text = re.sub(r"url=/", f"url={base_url}", text)

    # replace base url in sitemap.xml
    text = re.sub(r"<loc>/", f"<loc>{base_url}", text)

    return text
