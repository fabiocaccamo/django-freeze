# -*- coding: utf-8 -*-

from io import open
from io import BytesIO

import os
import shutil
import tempfile
import zipfile

from freeze import settings


def write(data, html_in_memory = False, zip_in_memory = False, zip_include_media = settings.FREEZE_ZIP_INCLUDE_MEDIA, zip_include_static = settings.FREEZE_ZIP_INCLUDE_STATIC):
    
    if os.path.exists(settings.FREEZE_ROOT):
        shutil.rmtree(settings.FREEZE_ROOT)
        
    if not os.path.exists(settings.FREEZE_ROOT):
        os.makedirs(settings.FREEZE_ROOT)
        
    #create html site tree
    html_root = tempfile.mkdtemp() if html_in_memory else settings.FREEZE_HTML_ROOT
    
    if html_in_memory:
        
        print(u'\ncreate html site tree and write it to a temporary directory...')
            
        html_root = tempfile.mkdtemp()
        
    else:
        
        print(u'\ncreate html site tree and write it to disk...')
        
        html_root = settings.FREEZE_HTML_ROOT
        
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
        
    if zip_in_memory:
        zip_file_stream = BytesIO()
        zip_file = zipfile.ZipFile(zip_file_stream, 'w')
    else:
        zip_file = zipfile.ZipFile(settings.FREEZE_ZIP_PATH, 'w')
    
    print(u'create file: %s' % (html_path, ))
    
    print(u'\nzip files...')
    
    #zip www
    for d in data:
        
        file_disk_path = os.path.normpath(html_root + d['html_path'])
        file_zip_path = d['html_path']
        
        print(u'zip file: %s' % (file_zip_path, ))
        
        zip_file.write(file_disk_path, file_zip_path)
        
    if zip_include_static:
        
        print(u'\nzip static files...')
        
        #zip static
        for root, dirs, files in os.walk(settings.FREEZE_STATIC_ROOT):
            
            for file in files:
                
                file_disk_path = os.path.join(root, file)
                file_zip_path = file_disk_path[file_disk_path.find(settings.FREEZE_STATIC_URL):]
                
                if settings.FREEZE_ZIP_INCLUDE_STATIC_APPS:
                    
                    file_app_name = file_zip_path.replace(settings.FREEZE_STATIC_URL, '').split('/')[0]
                    
                    for app_name in settings.FREEZE_ZIP_INCLUDE_STATIC_APPS:
                        
                        if app_name == file_app_name:
                            
                            print(u'zip static file: %s' % (file_zip_path, ))
                            
                            zip_file.write(file_disk_path, file_zip_path)
                            
                            break
                else:
                    
                    print(u'zip static file: %s' % (file_zip_path, ))
                    
                    zip_file.write(file_disk_path, file_zip_path)
                    
                    
    if zip_include_media:
        
        print(u'\nzip media files...')
        
        #zip media
        for root, dirs, files in os.walk(settings.FREEZE_MEDIA_ROOT):
            
            for file in files:
                
                file_disk_path = os.path.join(root, file)
                file_zip_path = file_disk_path[file_disk_path.find(settings.FREEZE_MEDIA_URL):]
                
                print(u'zip media file: %s' % (file_zip_path, ))
                
                zip_file.write(file_disk_path, file_zip_path)
                
                
    zip_file.close()
    
    if zip_in_memory:
        
        zip_file_stream.seek(0)
        return zip_file_stream.getvalue()
        
    else:
        
        print(u'\nzip file ready at: %s' % (settings.FREEZE_ZIP_PATH, ))
           
        return
        
        