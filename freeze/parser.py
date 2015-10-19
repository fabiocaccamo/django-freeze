# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse, NoReverseMatch

import os
import requests
import xmltodict

from bs4 import BeautifulSoup

from freeze import settings


def parse_sitemap_urls():
    
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
            sitemap_url = 'sitemap.xml'
            
    #load sitemap
    sitemap_url = settings.FREEZE_HOST + sitemap_url# + 'enforce404'
    sitemap_request = requests.get(sitemap_url)
    
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
    
    
def parse_html_urls(html, base_url = '/', media_urls = False, static_urls = False, external_urls = False):
    
    urls = []
    
    html_soup = BeautifulSoup(html, 'html5lib')
          
    for url_node in html_soup.findAll('a'):
        url = url_node.get('href')
        
        if url:
            url = url.replace(settings.FREEZE_HOST, u'')
            
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
                url = settings.FREEZE_HOST + url
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
                url = settings.FREEZE_HOST + url
                urls.append(url)
                
    urls = list(set(urls))
    urls.sort()
    
    return urls
    
    