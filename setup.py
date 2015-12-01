
#!/usr/bin/env python
from setuptools import setup

exec(open('freeze/version.py').read())


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
        'Django>=1.6.5,<1.9',
        'beautifulsoup4>=4.4.1',
        'requests>=2.8.0',
        'xmltodict>=0.9.2',
    ],
    classifiers=[]
)

