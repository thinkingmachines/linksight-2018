import json
import os.path
import uuid

import pandas as pd
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.db.models import Q

from linksight.api.psgc_code_matcher import PSGCCodeMatcher


class Dataset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    file = models.FileField(upload_to='datasets/')
    name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or self.file.name

    def preview(self, n=10):
        with self.file.open() as f:
            df = pd.read_csv(f)
            preview = json.loads(
                df.head(n).to_json(orient='table')
            )
            preview['schema'].pop('pandas_version')
        preview['file'] = {
            'name': self.name,
            'size': f.size,
            'rows': len(df),
            'url': self.file.url,
        }
        return preview


class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE,
                                related_name='matches')
    matched_dataset = models.ForeignKey(Dataset, on_delete=models.SET_NULL,
                                        related_name='+', null=True)

    barangay_col = models.CharField(max_length=256, blank=False)
    city_municipality_col = models.CharField(max_length=256, blank=False)
    province_col = models.CharField(max_length=256, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} ({})'.format(self.dataset.name, self.id)

    def clean_matches(self, matches):
        for col in matches:
            if col.endswith('score'):
                filler = 0
            else:
                filler = None
            matches[col] = matches[col].where(pd.notnull(matches[col]),
                                              filler)
        return matches

    def generate_match_items(self, **kwargs):
        psgc = Dataset.objects.get(pk=settings.PSGC_DATASET_ID)
        with psgc.file.open() as f:
            psgc_df = pd.read_csv(f, dtype={'code': object})

        with self.dataset.file.open() as f:
            dataset_df = pd.read_csv(f)

        matcher = PSGCCodeMatcher(
            psgc_df,
            dataset_df,
            barangay_col=kwargs['barangay_col'],
            city_municipality_col=kwargs['city_municipality_col'],
            province_col=kwargs['province_col'],
        )
        matches = matcher.get_matches(max_near_matches=3)
        matches = self.clean_matches(matches)

        for _, row in matches.iterrows():
            MatchItem.objects.create(match=self, **row.to_dict(), chosen=False)

    def save_choices(self, match_choices):
        self.items.all().update(chosen=False)
        self.items.filter(
            id__in=match_choices.values(),
        ).update(chosen=True)
        self.refresh_from_db()

        with self.dataset.file.open() as f:
            dataset_df = pd.read_csv(f)

        matches_df = pd.DataFrame(list(self.items.filter(
            Q(matched=True) | Q(chosen=True)
        ).values()))
        matches_df.set_index('dataset_index')

        joined_df = dataset_df.join(matches_df[[
            'matched_barangay',
            'matched_barangay_psgc_code',
            'matched_barangay_score',
            'matched_city_municipality',
            'matched_city_municipality_psgc_code',
            'matched_city_municipality_score',
            'matched_province',
            'matched_province_psgc_code',
            'matched_province_score',
            'total_score',
        ]])

        name, _ = os.path.splitext(self.dataset.name)
        self.matched_dataset = Dataset.objects.create(
            name='{}-matched.csv'.format(name),
        )
        file = ContentFile(joined_df.to_csv(index=False))
        self.matched_dataset.file.save(self.matched_dataset.name, file)
        self.save()

    def preview(self):
        return self.matched_dataset.preview()


class MatchItem(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, editable=False,
                              related_name='items')
    dataset_index = models.IntegerField(editable=False)

    source_barangay = models.CharField(
        max_length=256, editable=False, null=True)
    source_city_municipality = models.CharField(
        max_length=256, editable=False, null=True)
    source_province = models.CharField(
        max_length=256, editable=False, null=True)

    matched_barangay = models.CharField(
        max_length=256, editable=False, null=True)
    matched_barangay_psgc_code = models.IntegerField(
        editable=False, null=True)
    matched_barangay_score = models.FloatField(
        editable=False)

    matched_city_municipality = models.CharField(
        max_length=256, editable=False, null=True)
    matched_city_municipality_psgc_code = models.IntegerField(
        editable=False, null=True)
    matched_city_municipality_score = models.FloatField(
        editable=False)

    matched_province = models.CharField(
        max_length=256, editable=False, null=True)
    matched_province_psgc_code = models.IntegerField(
        editable=False, null=True)
    matched_province_score = models.FloatField(
        editable=False)

    total_score = models.FloatField(editable=False)

    matched = models.BooleanField(editable=False)
    chosen = models.BooleanField()

    class Meta:
        ordering = ['dataset_index', '-total_score']

