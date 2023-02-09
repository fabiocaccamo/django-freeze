from django.urls import path

from freeze.views import download_static_site, generate_static_site

urlpatterns = [
    path(
        "download-static-site/",
        download_static_site,
        name="freeze_download_static_site",
    ),
    path(
        "generate-static-site/",
        generate_static_site,
        name="freeze_generate_static_site",
    ),
]
