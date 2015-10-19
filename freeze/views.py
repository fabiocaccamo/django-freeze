# -*- coding: utf-8 -*-

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.http import HttpResponseServerError

from datetime import datetime

from freeze import settings, scanner, writer


def generate_static_site(request):
    
    if request.user and request.user.is_staff and request.user.is_active:
        
        try:
            data = scanner.scan(report_invalid_urls = False)
            value = writer.write(data, html_in_memory = True, zip_in_memory = True)
            
            #if zip_in_memory:
            response = HttpResponse(value, content_type = 'application/zip')
            #else:
            #   response = HttpResponse(open(settings.FREEZE_ZIP_PATH, 'r'), content_type = 'application/zip')
            
            prefix = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = settings.FREEZE_ZIP_NAME_WITH_PREFIX % (prefix, )
            
            response['Content-Disposition'] = 'attachment; filename=%s' % (filename, )
            return response
        
        except IOError:
            return HttpResponseServerError()
    else:
        raise PermissionDenied
        
        