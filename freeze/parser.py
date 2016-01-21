# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse, NoReverseMatch

import os
import re
import requests
import xmltodict

from bs4 import BeautifulSoup

from freeze import settings

    
def parse_sitemap_urls( site_url = settings.FREEZE_SITE_URL ):
    
    urls = []
    
    #reverse sitemap url
    sitemap_ok = False
    sitemap_url = None
    
    try:
        sitemap_url = reverse('django.contrib.sitemaps.views.sitemap')
    
    except NoReverseMatch:
        
        try:
            sitemap_url = reverse('sitemap')
            
        except NoReverseMatch:
            
            #raise NoReverseMatch('Reverse for \'django.contrib.sitemaps.views.sitemap\' or \'sitemap\' not found.')
            sitemap_url = '/sitemap.xml'
            
    #load sitemap
    sitemap_url = site_url + sitemap_url
    sitemap_request = requests.get(sitemap_url)
    sitemap_request.encoding = 'utf-8'
    
    if sitemap_request.status_code == requests.codes.ok:
        
        try:
            sitemap_data = xmltodict.parse(sitemap_request.text)
            sitemap_ok = True
        except:
            print(u'sitemap parsing error...')
    else:
        print(u'sitemap not founded...')
        
    if sitemap_ok:
        
        sitemap_urls_data = sitemap_data.get('urlset', {}).get('url', {})
        
        for sitemap_url_data in sitemap_urls_data:
            
            url = sitemap_url_data.get('loc', '')
            urls.append(url)
            
        urls = list(set(urls))
        urls.sort()
        
    return urls
    
    
def parse_html_urls(html, site_url = settings.FREEZE_SITE_URL, base_url = '/', media_urls = False, static_urls = False, external_urls = False):
    
    urls = []
    
    soup = BeautifulSoup(html, 'html5lib')

    for url_node in soup.findAll('a'):
        url = url_node.get('href')
        
        if url:
            url = url.replace(site_url, u'')
            
            if url.find(settings.FREEZE_MEDIA_URL) == 0 and not media_urls:
                #skip media files urls
                continue
                
            elif url.find(settings.FREEZE_STATIC_URL) == 0 and not static_urls:
                #skip static files urls
                continue
                
            elif url[0] == '#':
                #skip anchors
                continue
                
            elif url[0] == '/':
                #url already start from the site root
                url = site_url + url
                urls.append(url)
                continue
                
            elif ':' in url:
                #probably an external link or a link like tel: mailto: skype: call: etc...
                if external_urls and url.lower().find('http') == 0:
                    urls.append(url)
                else:
                    continue
            else:
                #since it's a relative url let's merge it with the current page path
                url = os.path.normpath(os.path.abspath(os.path.normpath(base_url + '/' + url)))
                url = site_url + url
                urls.append(url)
                
    urls = list(set(urls))
    urls.sort()
    
    return urls
    
    
def replace_base_url(text, base_url):
    
    if base_url != None:
        
        media_url = settings.FREEZE_MEDIA_URL

        if media_url.startswith('/'):
            
            #fix media double slashes mistake
            text = text.replace('/' + media_url, media_url)
            
            #replace base url for media urls outside quotes
            text = re.sub(r'([^\"\'\-\_\w\d])' + media_url, r'\1' + base_url + media_url[1:], text)
            
        #replace base url for static urls in case of urls without "" or ''
        static_url = settings.FREEZE_STATIC_URL
        
        if static_url.startswith('/'):
            
            #fix static double slashes mistake
            text = text.replace('/' + static_url, static_url)
            
            #replace base url for static urls outside quotes
            text = re.sub(r'([^\"\'\-\_\w\d])' + static_url, r'\1' + base_url + static_url[1:], text)
            
        #replace base url for all urls relative to root between "" or ''
        def sub_base_url(match_obj):
            
            startquote = match_obj.group(1)
            url = (match_obj.group(4) or '')
            endquote = match_obj.group(6)
            
            return startquote + base_url + url + endquote

        text = re.sub(r'(\")((\/)([^\/](\\\"|(?!\").)*)?)(\")', sub_base_url, text)
        text = re.sub(r'(\')((\/)([^\/](\\\'|(?!\').)*)?)(\')', sub_base_url, text)
        
        #replace base url in case of <meta http-equiv="refresh" content="0; url=/en/" />
        text = re.sub(r'url=/', 'url=' + base_url, text)
        
        #replace base url in sitemap.xml
        text = re.sub(r'<loc>/', '<loc>' + base_url, text)
        
        #print(text)

    return text

    