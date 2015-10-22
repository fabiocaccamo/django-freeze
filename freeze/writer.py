# -*- coding: utf-8 -*-

from io import open
from io import BytesIO

import os
import shutil
import tempfile
import zipfile

from freeze import settings


def write(data, include_media = settings.FREEZE_INCLUDE_MEDIA, include_static = settings.FREEZE_INCLUDE_STATIC, html_in_memory = False, zip_all = False, zip_in_memory = False):
    
    if os.path.exists(settings.FREEZE_ROOT):
        shutil.rmtree(settings.FREEZE_ROOT)
        
    if not os.path.exists(settings.FREEZE_ROOT):
        os.makedirs(settings.FREEZE_ROOT)
        
    #create html site tree
    html_root = tempfile.mkdtemp() if html_in_memory else settings.FREEZE_ROOT
    
    if html_in_memory:
        
        print(u'\ncreate html site tree and write it to a temporary directory...')
            
        html_root = tempfile.mkdtemp()
        
    else:
        
        print(u'\ncreate html site tree and write it to disk...')
        
        html_root = settings.FREEZE_ROOT
        
        if not os.path.exists(html_root):
            os.makedirs(html_root)
            
    #create directories tree and index(es).html files
    for d in data:
        
        html_dirs = os.path.join(os.path.normpath(html_root + d['path']))
        html_path = os.path.join(os.path.normpath(html_root + d['html_path']))
        html = d['html']
        
        if not os.path.exists(html_dirs):
            os.makedirs(html_dirs)
            
            #print(u'create directory: %s' % (html_dirs, ))
            
        print(u'create file: %s' % (html_path, ))
        
        index_file = open(html_path, 'wb')
        index_file.write(html)
        index_file.close()
        
        
    if zip_all:
        
        print(u'\nzip files...')
        
        if zip_in_memory:
            zip_file_stream = BytesIO()
            zip_file = zipfile.ZipFile(zip_file_stream, 'w')
        else:
            zip_file = zipfile.ZipFile(settings.FREEZE_ZIP_PATH, 'w')
            
    for d in data:
        
        file_src_path = os.path.normpath(html_root + d['html_path'])
        
        if zip_all:
            
            file_rel_path = d['html_path']
            
            print(u'zip file: %s' % (file_rel_path, ))
            
            zip_file.write(file_src_path, file_rel_path)
    
    
    if include_static:
        
        if zip_all:
            print(u'\nzip static files...')
        else:
            print(u'\ncopy static files...')
            
        for root, dirs, files in os.walk(settings.FREEZE_STATIC_ROOT):
            
            include_dir = False
            
            if settings.FREEZE_INCLUDE_STATIC_DIRS:
                
                for static_dir in settings.FREEZE_INCLUDE_STATIC_DIRS:
                    
                    if root.find(static_dir) == 0:
                        include_dir = True
                        break
            else:
                include_dir = True
                
            if not include_dir:
                continue
                
            for file in files:
                
                file_src_path = os.path.join(root, file)
                file_dst_path = file_src_path[file_src_path.find(settings.FREEZE_STATIC_URL):]
                
                if zip_all:
                    
                    print(u'zip static file: %s' % (file_dst_path, ))
                    
                    zip_file.write(file_src_path, file_dst_path)
                
                else:
                    
                    file_dst_path = os.path.normpath(settings.FREEZE_ROOT + '/' + file_dst_path)
                    file_dst_dirname = os.path.dirname(file_dst_path)
                    
                    print(u'copy static file: %s - %s' % (file_src_path, file_dst_path, ))
                    
                    if not os.path.exists(file_dst_dirname):
                        os.makedirs(file_dst_dirname)
                        
                    shutil.copy2(file_src_path, file_dst_path)
    
    if include_media:
        
        if zip_all:
            print(u'\nzip media files...')
        else:
            print(u'\ncopy media files...')
            
        for root, dirs, files in os.walk(settings.FREEZE_MEDIA_ROOT):
            
            for file in files:
                
                file_src_path = os.path.join(root, file)
                file_dst_path = file_src_path[file_src_path.find(settings.FREEZE_MEDIA_URL):]
                
                if zip_all:
                    
                    print(u'zip media file: %s' % (file_dst_path, ))
                    
                    zip_file.write(file_src_path, file_dst_path)
                
                else:
                    
                    file_dst_path = os.path.normpath(settings.FREEZE_ROOT + '/' + file_dst_path)
                    file_dst_dirname = os.path.dirname(file_dst_path)
                    
                    print(u'copy media file: %s - %s' % (file_src_path, file_dst_path, ))
                    
                    if not os.path.exists(file_dst_dirname):
                        os.makedirs(file_dst_dirname)
                        
                    shutil.copy2(file_src_path, file_dst_path)
                    
    if zip_all:
        
        zip_file.close()
        
        if zip_in_memory:
            
            zip_file_stream.seek(0)
            return zip_file_stream.getvalue()
            
        else:
            print(u'\nstatic site zipped ready at: %s' % (settings.FREEZE_ZIP_PATH, ))
    else:
        print(u'\nstatic site ready at: %s' % (settings.FREEZE_ROOT, ))
        
        