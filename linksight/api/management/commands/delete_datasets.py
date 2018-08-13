from django.core.management.base import BaseCommand

from linksight.api.models import Dataset


class Command(BaseCommand):
    help = 'Deletes the public datasets'

    def handle(self, *args, **options):
        Dataset.objects.filter(is_public_dataset=True).delete()
