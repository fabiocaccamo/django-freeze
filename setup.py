
#!/usr/bin/env python
from setuptools import setup

exec(open('freeze/version.py').read())

from freeze import __version__

setup(
    name='django-freeze',
    packages=['freeze'],
    include_package_data=True,
    license='MIT License',
    version=__version__,
    description='django-freeze converts your django site to a static one with one line of code',
    author='Fabio Caccamo',
    author_email='fabio.caccamo@gmail.com',
    url='https://github.com/fabiocaccamo/django-freeze',
    download_url='https://github.com/fabiocaccamo/django-freeze/archive/%s.tar.gz' % __version__,
    keywords=['django', 'freeze', 'static', 'site', 'generator', 'generate', 'convert', 'export', 'download', 'zip'],
    install_requires=[
        'Django>=1.6.5',
        'beautifulsoup4>=4.4.1',
        'requests>=2.8.0',
        'xmltodict>=0.9.2',
    ],
    classifiers=[
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python',
    ],
)

