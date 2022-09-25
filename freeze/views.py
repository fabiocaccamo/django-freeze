# -*- coding: utf-8 -*-

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.http import StreamingHttpResponse

from datetime import datetime

from freeze import scanner, settings, writer

from wsgiref.util import FileWrapper

import os


def download_static_site(request):
    if request.user and request.user.is_staff and request.user.is_active:
        try:
            include_media_get = request.GET.get("include_media")
            include_media_default = settings.FREEZE_INCLUDE_MEDIA

            if include_media_get == "0":
                include_media = False
            elif include_media_get == "1":
                include_media = include_media_default if include_media_default else True
            else:
                include_media = include_media_default

            include_static_get = request.GET.get("include_static")
            include_static_default = settings.FREEZE_INCLUDE_STATIC

            if include_static_get == "0":
                include_static = False
            elif include_static_get == "1":
                include_static = (
                    include_static_default if include_static_default else True
                )
            else:
                include_static = include_static_default

            writer.write(
                scanner.scan(),
                include_media=include_media,
                include_static=include_static,
                html_in_memory=True,
                zip_all=True,
                zip_in_memory=False,
            )

            file_name_prefix = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = "%s_%s" % (
                file_name_prefix,
                settings.FREEZE_ZIP_NAME,
            )

            return download_zip(name=file_name)

        except:
            return HttpResponseServerError()
    else:
        raise PermissionDenied


def download_zip(path=settings.FREEZE_ZIP_PATH, name=settings.FREEZE_ZIP_NAME):
    # http://stackoverflow.com/questions/8600843/serving-large-files-with-high-loads-in-django
    response = StreamingHttpResponse(
        FileWrapper(open(path), 8192), content_type="application/zip"
    )
    response["Content-Length"] = os.path.getsize(path)
    response["Content-Disposition"] = "attachment; filename=%s" % (name,)
    return response


def generate_static_site(request):
    if request.user and request.user.is_staff and request.user.is_active:
        try:
            writer.write(
                scanner.scan(),
                html_in_memory=settings.FREEZE_ZIP_ALL,
                zip_all=settings.FREEZE_ZIP_ALL,
                zip_in_memory=False,
            )
            return HttpResponse()
        except IOError:
            return HttpResponseServerError()
    else:
        raise PermissionDenied
