import json
import os.path
import uuid
from collections import OrderedDict
from functools import partial

import pandas as pd

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.db.models import Q
from linksight.api.matchers.search_tuple import create_search_tuple, to_index
from linksight.api.tasks import match_dataset


class Dataset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 related_name='datasets',
                                 null=True)
    file = models.FileField(upload_to='datasets/')
    name = models.CharField(max_length=255, null=True)
    is_internal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or self.file.name

    def preview(self, n=10, match=None):
        with self.file.open() as f:
            df = pd.read_csv(f, dtype=str)
            preview = json.loads(
                df.head(n).to_json(orient='table')
            )
            preview['schema'].pop('pandas_version')
        preview['file'] = {
            'name': self.name,
            'size': f.size,
            'rows': len(df),
            'rowsShown': n,
            'url': self.file.url,
        }
        if match:
            preview['match'] = {
                'barangayCol': match.source_bgy_col,
                'cityMunicipalityCol': match.source_municity_col,
                'provinceCol': match.source_prov_col,
            }
        return preview


class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE,
                                related_name='matches')
    matched_dataset = models.ForeignKey(Dataset, on_delete=models.SET_NULL,
                                        related_name='+', null=True)

    source_bgy_col = models.CharField(max_length=256, blank=False, null=True)

    source_municity_col = models.CharField(max_length=256, blank=False, null=True)

    source_prov_col = models.CharField(max_length=256, blank=False, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} ({})'.format(self.dataset.name, self.id)

    @property
    def loc_columns(self):
        return OrderedDict([
            ('bgy', self.source_bgy_col),
            ('municity', self.source_municity_col),
            ('prov', self.source_prov_col),
        ])

    def match_dataset(self, **kwargs):
        result = match_dataset.apply_async((self.id,), expires=360)
        result.get()


    def save_choices(self, match_choices):

        # Save choices

        self.items.all().update(chosen=False)
        self.items.filter(
            id__in=match_choices.values(),
        ).update(chosen=True)
        self.refresh_from_db()

        # Merge matches

        with self.dataset.file.open() as f:
            dataset_df = pd.read_csv(f, dtype=str)

        dataset_df.set_index(
            dataset_df
            .apply(
                partial(create_search_tuple, columns=self.loc_columns),
                axis=1)
            .apply(to_index),
            inplace=True)

        matches_df = pd.DataFrame(list(self.items.filter(
            Q(match_type='exact') | Q(chosen=True)
        ).values()))
        matches_df.set_index('search_tuple', inplace=True)

        matches_df.rename(columns={
            'matched_barangay': 'bgy_linksight',
            'matched_city_municipality': 'municity_linksight',
            'matched_province': 'prov_linksight',
            'code': 'psgc_linksight',
            'total_score': 'confidence_score_linksight'
        }, inplace=True)

        # Rename some columns for display
        linksight_cols = [
            'bgy_linksight',
            'municity_linksight',
            'prov_linksight',
            'psgc_linksight',
            'confidence_score_linksight'
        ]

        dataset_df.drop(linksight_cols, axis=1, errors='ignore', inplace=True)
        joined_df = dataset_df.join(matches_df[linksight_cols])

        # Order columns

        front_cols = []
        for source_col, matched_col in (
            (self.source_bgy_col, 'bgy_linksight'),
            (self.source_municity_col, 'municity_linksight'),
            (self.source_prov_col, 'prov_linksight'),
        ):
            if source_col == matched_col:
                front_cols.extend((matched_col,))
            else:
                front_cols.extend((source_col, matched_col))

        mid_cols = [
            "psgc_linksight",
            "confidence_score_linksight"
        ]

        other_cols = [col for col in joined_df.columns.tolist()
                      if (col not in front_cols) and (col not in mid_cols)]
        new_cols = front_cols + mid_cols + other_cols
        joined_df = joined_df[new_cols]

        # Create matched dataset

        name, _ = os.path.splitext(self.dataset.name)
        self.matched_dataset = Dataset.objects.create(
            name='{}-linksight.csv'.format(name),
        )
        file = ContentFile(joined_df.to_csv(index=False).encode('utf-8'))
        self.matched_dataset.file.save(self.matched_dataset.name, file)
        self.save()


class MatchItem(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, editable=False,
                              related_name='items')

    dataset_index = models.IntegerField(editable=False)

    search_tuple = models.CharField(
        max_length=256, db_index=True)

    source_barangay = models.CharField(
        max_length=256, editable=False, null=True)
    source_city_municipality = models.CharField(
        max_length=256, editable=False, null=True)
    source_province = models.CharField(
        max_length=256, editable=False, null=True)

    matched_barangay = models.CharField(
        max_length=256, editable=False, null=True)
    matched_city_municipality = models.CharField(
        max_length=256, editable=False, null=True)
    matched_province = models.CharField(
        max_length=256, editable=False, null=True)

    code = models.CharField(
        max_length=256, editable=False, null=True)
    total_score = models.FloatField(editable=False)

    match_types = (
        ('no_match', 'No Match'),
        ('near', 'Partial/Near Match'),
        ('exact', 'Exact Match'),
    )
    match_type = models.CharField(
        max_length=25,
        choices=match_types,
        default='no_match'
    )
    match_time = models.FloatField()

    chosen = models.BooleanField()

    class Meta:
        ordering = ['dataset_index', '-total_score']
