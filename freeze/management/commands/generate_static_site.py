# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from freeze import scanner, settings, writer


class Command(BaseCommand):
    
    help = u'Generate static site.'
    
    def handle(self, **options):
        
        writer.write( scanner.scan(), html_in_memory = settings.FREEZE_ZIP_ALL, zip_all = settings.FREEZE_ZIP_ALL, zip_in_memory = False)
        
        return
        
        