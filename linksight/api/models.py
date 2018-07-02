import json
import uuid

import pandas as pd

from django.db import models


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
        }
        return preview


class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE,
                                related_name='matches')

    barangay_col = models.CharField(max_length=256, blank=False)
    city_municipality_col = models.CharField(max_length=256, blank=False)
    province_col = models.CharField(max_length=256, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} ({})'.format(self.dataset.name, self.id)


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

    matched_municipality_city = models.CharField(
        max_length=256, editable=False, null=True)
    matched_municipality_city_psgc_code = models.IntegerField(
        editable=False, null=True)
    matched_municipality_city_score = models.FloatField(
        editable=False)

    matched_province = models.CharField(
        max_length=256, editable=False, null=True)
    matched_province_psgc_code = models.IntegerField(
        editable=False, null=True)
    matched_province_score = models.FloatField(
        editable=False)

    total_score = models.FloatField(editable=False)

    matched = models.BooleanField(editable=False)
    chosen = models.NullBooleanField(null=True)
