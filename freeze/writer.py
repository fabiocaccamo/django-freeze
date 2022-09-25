# -*- coding: utf-8 -*-

from io import open
from io import BytesIO

import os
import shutil
import tempfile
import zipfile

from freeze import settings


def write(
    data,
    include_media=settings.FREEZE_INCLUDE_MEDIA,
    include_static=settings.FREEZE_INCLUDE_STATIC,
    html_in_memory=False,
    zip_all=settings.FREEZE_ZIP_ALL,
    zip_in_memory=False,
):

    if os.path.exists(settings.FREEZE_ROOT):
        shutil.rmtree(settings.FREEZE_ROOT)

    if not os.path.exists(settings.FREEZE_ROOT):
        os.makedirs(settings.FREEZE_ROOT)

    # create site tree
    files_root = tempfile.mkdtemp() if html_in_memory else settings.FREEZE_ROOT

    if html_in_memory:
        print("\ncreate site tree and write it to a temporary directory...")
        files_root = tempfile.mkdtemp()
    else:
        print("\ncreate site tree and write it to disk...")
        files_root = settings.FREEZE_ROOT
        if not os.path.exists(files_root):
            os.makedirs(files_root)

    # create directories tree and index(es).html files
    for d in data:
        file_dirs = os.path.join(os.path.normpath(files_root + d["file_dirs"]))
        file_path = os.path.join(os.path.normpath(files_root + d["file_path"]))
        file_data = d["file_data"]
        if not os.path.exists(file_dirs):
            os.makedirs(file_dirs)
            # print(u'create directory: %s' % (file_dirs, ))

        print("create file: %s" % (file_path,))
        file_obj = open(file_path, "wb")
        encoded_file_data = file_data
        try:
            encoded_file_data = bytes(file_data, "utf-8")
        except TypeError:
            pass

        file_obj.write(encoded_file_data)
        file_obj.close()

    if zip_all:
        print("\nzip files...")
        if zip_in_memory:
            zip_file_stream = BytesIO()
            zip_file = zipfile.ZipFile(zip_file_stream, "w")
        else:
            zip_file = zipfile.ZipFile(settings.FREEZE_ZIP_PATH, "w")

    for d in data:
        file_src_path = os.path.normpath(files_root + d["file_path"])
        if zip_all:
            file_rel_path = d["file_path"]
            print("zip file: %s" % (file_rel_path,))
            zip_file.write(file_src_path, file_rel_path)

    if include_static:
        if zip_all:
            print("\nzip static files...")
        else:
            print("\ncopy static files...")

        include_static_dirs = isinstance(include_static, (list, tuple))

        for root, dirs, files in os.walk(settings.FREEZE_STATIC_ROOT):
            include_dir = False
            if include_static_dirs:
                for static_dir in include_static:
                    static_dir_path = os.path.join(
                        settings.FREEZE_STATIC_ROOT + static_dir
                    )
                    if root.find(static_dir_path) == 0:
                        include_dir = True
                        break
            else:
                include_dir = True

            if not include_dir:
                continue

            for file in files:
                file_src_path = os.path.join(root, file)
                file_dst_path = file_src_path[
                    file_src_path.find(settings.FREEZE_STATIC_URL) :
                ]

                if zip_all:
                    print("zip static file: %s" % (file_dst_path,))
                    zip_file.write(file_src_path, file_dst_path)
                else:
                    file_dst_path = os.path.normpath(
                        settings.FREEZE_ROOT + "/" + file_dst_path
                    )
                    file_dst_dirname = os.path.dirname(file_dst_path)
                    print("copy static file: %s - %s" % (file_src_path, file_dst_path))

                    if not os.path.exists(file_dst_dirname):
                        os.makedirs(file_dst_dirname)

                    shutil.copy2(file_src_path, file_dst_path)

    if include_media:
        if zip_all:
            print("\nzip media files...")
        else:
            print("\ncopy media files...")

        include_media_dirs = isinstance(include_media, (list, tuple))
        for root, dirs, files in os.walk(settings.FREEZE_MEDIA_ROOT):
            include_dir = False
            if include_media_dirs:
                for media_dir in include_media:
                    media_dir_path = os.path.join(
                        settings.FREEZE_MEDIA_ROOT + media_dir
                    )
                    if root.find(media_dir_path) == 0:
                        include_dir = True
                        break
            else:
                include_dir = True

            if not include_dir:
                continue

            for file in files:
                file_src_path = os.path.join(root, file)
                file_dst_path = file_src_path[
                    file_src_path.find(settings.FREEZE_MEDIA_URL) :
                ]
                if zip_all:
                    print("zip media file: %s" % (file_dst_path,))
                    zip_file.write(file_src_path, file_dst_path)
                else:
                    file_dst_path = os.path.normpath(
                        settings.FREEZE_ROOT + "/" + file_dst_path
                    )
                    file_dst_dirname = os.path.dirname(file_dst_path)
                    print("copy media file: %s - %s" % (file_src_path, file_dst_path))

                    if not os.path.exists(file_dst_dirname):
                        os.makedirs(file_dst_dirname)

                    shutil.copy2(file_src_path, file_dst_path)

    if zip_all:
        zip_file.close()
        if zip_in_memory:
            zip_file_stream.seek(0)
            zip_file_stream_value = zip_file_stream.getvalue()
            zip_file_stream.close()
            return zip_file_stream_value
        else:
            print("\nstatic site zipped ready at: %s" % (settings.FREEZE_ZIP_PATH,))
    else:
        print("\nstatic site ready at: %s" % (settings.FREEZE_ROOT,))
