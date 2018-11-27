from datetime import timedelta

from api.models import Dataset
from django.core.management.base import BaseCommand
from django.utils import timezone

THRESHOLD = 24


class Command(BaseCommand):
    help = 'Deletes the public datasets that are older than 24 hours'

    def handle(self, *args, **options):
        time_threshold = timezone.now() - timedelta(hours=THRESHOLD)
        Dataset.objects.filter(is_internal=False,
                               created_at__lt=time_threshold).delete()
