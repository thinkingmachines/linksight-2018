from django.core.management.base import BaseCommand, CommandError

from linksight.api.models import Dataset, Match


class Command(BaseCommand):
    help = 'Deletes the public datasets'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write('delete datasets')
