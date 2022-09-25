# -*- coding: utf-8 -*-

from django.core.mail import mail_managers
from django.template.loader import render_to_string

import os
import requests

from freeze import settings, parser


def scan(
    site_url=settings.FREEZE_SITE_URL,
    base_url=settings.FREEZE_BASE_URL,
    relative_urls=settings.FREEZE_RELATIVE_URLS,
    local_urls=settings.FREEZE_LOCAL_URLS,
    follow_sitemap_urls=settings.FREEZE_FOLLOW_SITEMAP_URLS,
    follow_html_urls=settings.FREEZE_FOLLOW_HTML_URLS,
    report_invalid_urls=settings.FREEZE_REPORT_INVALID_URLS,
    request_headers=settings.FREEZE_REQUEST_HEADERS,
):

    if site_url.endswith("/"):
        site_url = site_url[0:-1]

    home_url = site_url + "/"
    sitemap_urls = parser.parse_sitemap_urls()

    urls_data = []
    urls = [home_url]

    if follow_sitemap_urls:
        urls += sitemap_urls

    memo = []
    errs = []

    print("fetch urls...")

    def scan_error(req):

        err = "[ERROR %s]" % (req.status_code,)
        errs.append(
            "%s %s"
            % (
                err,
                req.url,
            )
        )

        print(err)

    def scan_url(url):

        if url.find(site_url) == 0:

            # clean only static-site urls
            url_qm = url.find("?")
            if url_qm > -1:
                url = url[0:url_qm]

            url_hash = url.find("#")
            if url_hash > -1:
                url = url[0:url_hash]

        if not url in memo:
            memo.append(url)
        else:
            return

        print("\nfetch url: %s" % (url,))

        req = requests.get(url, headers=request_headers)
        req.encoding = "utf-8"

        if req.status_code == requests.codes.ok:

            if req.url.find(site_url) != 0:
                # skip non static-site urls (external links)
                return

            is_redirect = req.url != url and req.history

            if is_redirect:

                if req.url.find(site_url) != 0:
                    # redirected to a page of another domain
                    print("[OK DONT FOLLOW REDIRECT] -> %s" % (req.url,))
                    return

                redirect_url = req.url.replace(site_url, "")
                html_data = {
                    "redirect_url": redirect_url,
                    "local_urls": settings.FREEZE_LOCAL_URLS,
                }

                html_str = render_to_string("freeze/redirect.html", html_data)
                html = "%s" % (html_str,)
                print("[OK FOLLOW REDIRECT] -> %s" % (req.url,))

            else:

                html = "%s" % (req.text,)
                html = html.replace(site_url, "")
                html = html.strip()

                if local_urls:
                    # prevent local directory index
                    html = html.replace(
                        "</body>",
                        "<script>"
                        + render_to_string("freeze/js/local_urls.js")
                        + "</script></body>",
                    )

                html = html.encode("utf-8")
                print("[OK]")

            path = os.path.normpath(url.replace(site_url, ""))

            if path.endswith(".html"):
                # print('path (HTML) -> ' + path)
                file_slash = path.rfind("/") + 1
                file_dirs = path[0:file_slash]
                file_name = path[file_slash:]
            else:
                # print('path -> ' + path)
                file_dirs = path
                file_name = "index.html"

            file_path = os.path.join(file_dirs, file_name)
            file_base_url = base_url

            if relative_urls:
                file_depth = len(list(filter(bool, file_dirs.split("/"))))
                if file_depth > 0:
                    file_base_url = "../" * file_depth
                else:
                    file_base_url = ""

            file_data = parser.replace_base_url(html, file_base_url)

            # print('file dirs: ' + file_dirs)
            # print('file name: ' + file_name)
            # print('file path: ' + file_path)
            # print('file base url: ' + file_base_url)
            # print('file data: ' + file_data)
            # print('---')

            urls_data.append(
                {
                    "url": url,
                    "file_dirs": file_dirs,
                    "file_path": file_path,
                    "file_data": file_data,
                }
            )

            if is_redirect:
                scan_url(req.url)
            else:
                if follow_html_urls:
                    html_urls = parser.parse_html_urls(
                        html=html,
                        site_url=site_url,
                        base_url=path,
                        media_urls=False,
                        static_urls=False,
                        external_urls=False,
                    )
                    for url in html_urls:
                        scan_url(url)
        else:
            scan_error(req)

    for url in urls:
        scan_url(url)

    urls_data.sort(key=lambda d: d["url"])

    errs = list(set(errs))
    errs.sort()

    if report_invalid_urls:
        mail_managers(settings.FREEZE_REPORT_INVALID_URLS_SUBJECT, "\n".join(errs))

    return urls_data
