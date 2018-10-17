from celery import shared_task
from linksight.api.matchers.ngrams_matcher import NgramsMatcher


@shared_task
def match_dataset(match_id):
    from linksight.api.models import Match, MatchItem
    match = Match.objects.get(pk=match_id)
    matcher = NgramsMatcher(dataset_file=match.dataset.file,
                            columns=match.loc_columns)
    matches = matcher.get_matches()
    MatchItem.objects.bulk_create([
        MatchItem(**match_item, match=match, chosen=False)
        for match_item in matches
    ])
