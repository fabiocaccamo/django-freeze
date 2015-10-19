# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from freeze import scanner, writer


class Command(BaseCommand):
    
    help = u'Generate static site and zip it.'
    
    def handle(self, **options):
        
        data = scanner.scan()
        
        writer.write(data, html_in_memory = True)
        
        return
        
        