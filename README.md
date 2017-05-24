# django-freeze
django-freeze generates the static version of your django site.

Just run ``python manage.py generate_static_site`` :)

## Features

- **Generate** the **static version** of your Django site, optionally compressed **.zip file**
- **Generate/download** the static site using **urls** *(only superuser and staff)*
- Follow **sitemap.xml** urls
- Follow **internal links** founded in each page
- Follow **redirects**
- **Report** invalid/broken urls
- Selectively **include/exclude media and static files**
- Custom **base url** *(very useful if the static site will run in a specific folder different by the document-root)*
- Convert urls to **relative urls** *(very useful if the static site will run offline or in an unknown folder different by the document-root)*
- Prevent local directory index

## Requirements / Dependencies
- Python 2.6, Python 2.7, Python 3.5
- Django 1.6.5 through Django 1.10
- BeautifulSoup4
- requests
- xmltodict

## Installation
- Run ``pip install django-freeze`` or manually download [django-freeze](https://pypi.python.org/pypi/django-freeze), [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4), 
[requests](https://pypi.python.org/pypi/requests/), [xmltodict](https://pypi.python.org/pypi/xmltodict)
- Add ``freeze`` to ``settings.INSTALLED_APPS``
- Restart your application server

## Configuration (optional)

All these settings are optional, if not defined in ``settings.py`` the default values (listed below) will be used.

```python

#the absolute path where to store the .zip and the html files
#default value is a folder named 'freeze' located as sibling of 'settings.MEDIA_ROOT'
FREEZE_ROOT = '/...' 

#tells 'freeze' if the urls should be fetched using https instead of http protocol (only if FREEZE_SITE_URL is not defined)
FREEZE_USE_HTTPS = False

#the site-url to crawl, if not specified it will be autodetected using the sites app
FREEZE_SITE_URL = 'http://mydomain.com'

#the base-url for all links relative to root '/'
#useful if the generated static site will run in a specific folder which is not the document-root
FREEZE_BASE_URL = None

#if True 'freeze' will convert all absolute urls to relative urls
#useful if the generated static site will run locally (file://) or in an unknown folder which is not the document-root (only if FREEZE_BASE_URL is not defined)
FREEZE_RELATIVE_URLS = False

#if True 'freeze' will inject a script at the end of each page
#which will force hrefs like 'path/' to 'path/index.html' (only if the site is running under file://)
#useful if the generated static site will run locally (requires FREEZE_RELATIVE_URLS set to True) to prevent local directory index
FREEZE_LOCAL_URLS = False

#if True 'freeze' will fetch each url founded in sitemap.xml
FREEZE_FOLLOW_SITEMAP_URLS = True

#if True 'freeze' will follow and fetch recursively each link-url founded in each page
FREEZE_FOLLOW_HTML_URLS = True

#if true 'freeze' will send an email to managers containing the list of all invalid urls (404, 500, etc..)
FREEZE_REPORT_INVALID_URLS = False

#the invalid urls email report subject
FREEZE_REPORT_INVALID_URLS_SUBJECT = '[freeze] invalid urls'

#if True the generated site will contain also the MEDIA folder and ALL its content
FREEZE_INCLUDE_MEDIA = True
#elif the value is a list or tuple only the specified directories will be included
FREEZE_INCLUDE_MEDIA = ('cache', 'images', 'videos', )

#if True the generated site will contain also the STATIC folder and ALL its content
FREEZE_INCLUDE_STATIC = True
#elif the value is a list or tuple only the specified directories will be included
FREEZE_INCLUDE_STATIC = ('myapp1', 'myapp2', 'myapp3', )

#if True the generated site will be zipped, the *.zip file will be created in FREEZE_ROOT
FREEZE_ZIP_ALL = False

#the name of the zip file created
FREEZE_ZIP_NAME = 'freeze'

#The request headers to use during the get requests that scrape the site
#can be used to set Authentication headers, by default sets the user-agent
FREEZE_REQUEST_HEADERS = {'user-agent': 'django-freeze'}

```
Add **freeze.urls** to ``urls.py`` if you want superusers and staff able to use freeze urls.

```python
urlpatterns = patterns('',
    ...
    url(r'^freeze/', include('freeze.urls')),
    ...
)
```

## Usage

#### Terminal

Run ``python manage.py generate_static_site`` 

#### URLs
Superusers and staff can use the following urls to **download a .zip** containing the generated static site or to just generate the static website.

``/freeze/download-static-site/``

``/freeze/generate-static-site/``

*(the time necessary to generate the static site depends on the size of the project)*

## TODO
- Write tests
- Add sitemap.xml and robots.txt to the generated static site

## License
Released under [MIT License](LICENSE).
