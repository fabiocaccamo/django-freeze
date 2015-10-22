# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from freeze import controller


class Command(BaseCommand):
    
    help = u'Generate static site.'
    
    def handle(self, **options):
        
        controller.generate_static_site()
        
        return
        
        