
#!/usr/bin/env python
from setuptools import setup, find_packages

exec(open('freeze/version.py').read())



setup(
    name='django-freeze',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    version=__version__,
    description='django-freeze generates the static version of any site.',
    author='Fabio Caccamo',
    author_email='fabio.caccamo@gmail.com',
    url='https://github.com/fabiocaccamo/django-freeze',
    download_url='https://github.com/fabiocaccamo/django-freeze/archive/%s.tar.gz' % __version__,
    keywords=['django', 'freeze', 'static', 'site', 'generator', 'generate', 'convert', 'export', 'download', 'zip'],
    install_requires=[
        'Django>=1.6.5,<1.9',
        'BeautifulSoup>=3.2.1',
        'requests>=2.8.0',
        'xmltodict>=0.9.2',
    ],
    include_package_data=True,
    classifiers=[]
)

