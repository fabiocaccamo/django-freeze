# -*- coding: utf-8 -*-

from django.core.mail import mail_managers
from django.template.loader import render_to_string

import os
import requests

from freeze import settings, parser


def scan( sitemap_mode = settings.FREEZE_SITEMAP_MODE, follow_mode = settings.FREEZE_FOLLOW_MODE, report_invalid_urls = settings.FREEZE_REPORT_INVALID_URLS ):
    
    data = []
    
    urls = [ settings.FREEZE_HOST + ('/' if settings.FREEZE_DOMAIN[-1] != '/' else '') ] 
    
    if sitemap_mode:
        
        urls += parser.parse_sitemap_urls()
    
    memo = []
    errs = []
    
    print(u'fetch urls...')
        
    #extract data for a given url
    def scan_url( url ):
        
        if url.find(settings.FREEZE_HOST) == 0:
            
            #clean only static-site urls
            url_qm = url.find('?')
            
            if url_qm > -1:
                url = url[0:url_qm]
                
            url_hash = url.find('#')
            
            if url_hash > -1:
                url = url[0:url_hash]
                
            if url[-1] != '/':
                url += '/'
                
        if not url in memo:
            memo.append(url)
        else:
            return
            
        print(u'\nfetch url: %s' % (url, ))
        
        req = requests.get(url)
        req.encoding = 'utf-8'
        
        if req.status_code == requests.codes.ok:
            
            if req.url.find(settings.FREEZE_HOST) != 0:
                #skip non static-site urls (external links)
                return
            
            is_redirect = (req.url != url and req.history)
            
            if is_redirect:
                
                if req.url.find(settings.FREEZE_HOST) != 0:
                    #redirected to a page of another domain
                    print(u'[OK DONT FOLLOW REDIRECT] -> %s' % (req.url, ))
                    
                    return
                    
                html_str = render_to_string('freeze/redirect.html', { 'redirect_url':req.url.replace(settings.FREEZE_HOST, u'') })
                html = u'%s' % (html_str, )
                
                print(u'[OK FOLLOW REDIRECT] -> %s' % (req.url, ))
            
            else:
                
                html = u'%s' % (req.text, )
                html = html.replace(settings.FREEZE_HOST, u'')
                html = html.strip()
                html = html.encode('utf-8')
                
                print(u'[OK]')
                
            path = os.path.normpath(url.replace(settings.FREEZE_HOST, ''))
            
            html_path = os.path.join(path, 'index.html')
            
            data.append({ 
                'url': url, 
                'path': path, 
                'html': html, 
                'html_path': html_path, 
            })
            
            if is_redirect:
                
                scan_url(req.url)
                
            else:
                
                if follow_mode:
                    
                    html_urls = parser.parse_html_urls(html = html, base_url = path, media_urls = False, static_urls = False, external_urls = False)
                    
                    for url in html_urls:
                        
                        scan_url(url)
        else:
            
            err = u'[ERROR %s]' % (req.status_code, )
            errs.append(u'%s %s' % (err, req.url, ))
            
            print(err)
                
    for url in urls:
        scan_url(url)
        
    data.sort(key = lambda d: d['url'])
    
    errs = list(set(errs))
    errs.sort()
    
    if report_invalid_urls:
        
        mail_managers(settings.FREEZE_REPORT_INVALID_URLS_SUBJECT, u'\n'.join(errs))
        
    return data
    
    