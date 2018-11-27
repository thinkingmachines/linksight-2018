from celery import shared_task
from django.conf import settings

from api.matchers.imatch_matcher import IMatchMatcher


@shared_task
def match_dataset(match_id):
    from api.models import Match, MatchItem
    match = Match.objects.get(pk=match_id)
    matcher = IMatchMatcher(
        dataset_file=match.dataset.file,
        columns=match.loc_columns,
        endpoint=settings.IMATCH_ENDPOINT,
        shared_dir=settings.IMATCH_SHARED_DIR,
    )
    matches = matcher.get_matches()
    MatchItem.objects.bulk_create([
        MatchItem(**match_item, match=match, chosen=False)
        for match_item in matches
    ])
