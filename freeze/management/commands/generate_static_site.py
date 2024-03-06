from django.conf import settings
from django.core.management.base import BaseCommand

from freeze import scanner, writer


class Command(BaseCommand):
    help = "Generate static site."

    def handle(self, **options):
        writer.write(
            scanner.scan(),
            html_in_memory=settings.FREEZE_ZIP_ALL,
            zip_all=settings.FREEZE_ZIP_ALL,
            zip_in_memory=False,
        )
        return
