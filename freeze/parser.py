# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse, NoReverseMatch

import os
import re
import requests
import xmltodict

from bs4 import BeautifulSoup

from freeze import settings


def parse_request_text( req ):
    
    text = u'%s' % (req.text, )
    text = text.replace(settings.FREEZE_HOST, u'')
    text = text.strip()
    text = text.encode('utf-8')
    
    return text
    
    
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
    sitemap_url = settings.FREEZE_HOST + sitemap_url
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
        
    return (sitemap_url, urls, )
    
    
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
    
    
re_double_quotes = re.compile(r'(\")((\/)([^\/](\\\"|(?!\").)*)?)(\")')
re_single_quotes = re.compile(r'(\')((\/)([^\/](\\\'|(?!\').)*)?)(\')')


def __replace_base_url( match_obj ):
    
    startquote = match_obj.group(1)
    url = (match_obj.group(4) or '')
    endquote = match_obj.group(6)
    
    return startquote + base_url + url + endquote


def replace_base_url(text, base_url):
    
    if base_url != None:
        
        text = re.sub(re_double_quotes, __replace_base_url, text)
        text = re.sub(re_single_quotes, __replace_base_url, text)
        text = re.sub(r'url=/', 'url=' + base_url, text) #<meta http-equiv="refresh" content="0; url=/en/" />
        text = re.sub(r'<loc>/', '<loc>' + base_url, text) #sitemap.xml urls
        #print(text)

    return text
    
    