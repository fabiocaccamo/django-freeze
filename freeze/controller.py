# -*- coding: utf-8 -*-

from freeze import scanner, settings, writer


def download_static_site():
    
    data = scanner.scan()
    value = writer.write(data, html_in_memory = True, zip_all = True, zip_in_memory = True)
    return value
    
        
def generate_static_site():
    
    data = scanner.scan()
    writer.write(data, html_in_memory = settings.FREEZE_ZIP_ALL, zip_all = settings.FREEZE_ZIP_ALL, zip_in_memory = False)
    
    