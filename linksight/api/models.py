import json
import os.path
import uuid

import pandas as pd

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.db.models import Q
from linksight.api.matcher import get_matches
from linksight.api.matcher import create_search_tuple


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
                'barangayCol': match.barangay_col,
                'cityMunicipalityCol': match.city_municipality_col,
                'provinceCol': match.province_col,
            }
        return preview


class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE,
                                related_name='matches')
    matched_dataset = models.ForeignKey(Dataset, on_delete=models.SET_NULL,
                                        related_name='+', null=True)

    barangay_col = models.CharField(max_length=256, blank=False, null=True)

    city_municipality_col = models.CharField(max_length=256, blank=False,
                                             null=True)
    province_col = models.CharField(max_length=256, blank=False, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} ({})'.format(self.dataset.name, self.id)

    def generate_match_items(self, **kwargs):
        with self.dataset.file.open() as f:
            dataset_df = pd.read_csv(f)

        
        columns = {
            'bgy': self.barangay_col,
            'municity': self.city_municipality_col,
            'prov': self.province_col,
        }

        MatchItem.objects.bulk_create([
            MatchItem(**match_item, match=self, chosen=False)
            for match_item in get_matches(dataset_df, columns=columns)
        ])

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
            dataset_df['search_tuple'] = dataset_df.apply(partial(create_search_tuple, columns=columns), axis=1)

        matches_df = pd.DataFrame(list(self.items.filter(
            Q(match_type='exact') | Q(chosen=True)
        ).values()))

        matches_df.set_index('search_tuple', inplace=True)

        print(matches_df.columns)

        joined_df = dataset_df.join(matches_df[[
            'matched_barangay',
            'matched_city_municipality',
            'matched_province',
            'code',
            'total_score'
        ]].dropna(axis=1,how="all"))


        # Get deepest PSGC

        # def get_deepest_code(row):
        #     for field in ['barangay', 'city_municipality', 'province']:
        #         key = 'matched_{}_psgc'.format(field)
        #         if row.get(key):
        #             return row[key]

        # joined_df['PSGC'] = joined_df.apply(
        #     get_deepest_code, axis=1).astype(str)

        # Merge population

        # population = Dataset.objects.get(pk=settings.POPULATION_DATASET_ID)
        # with population.file.open() as f:
        #     population_df = pd.read_csv(f, dtype={'Code': object})

        # joined_df = joined_df.merge(population_df, how='left',
        #                             left_on='PSGC', right_on='Code',
        #                             suffixes=[' (Source)', ''])
        # joined_df.drop([
        #     'Code',
        #     'matched_barangay_psgc',
        #     'matched_city_municipality_psgc',
        #     'matched_province_psgc',
        # ], axis='columns', inplace=True)

        # Reorder so matched columns and merged datasets are in front

        front_cols = []
        for source_col, matched_col in (
            (self.barangay_col, 'matched_barangay'),
            (self.city_municipality_col, 'matched_city_municipality'),
            (self.province_col, 'matched_province'),
        ):
             if source_col:
                 front_cols.extend((source_col, matched_col))
        # front_cols.extend([
        #     'PSGC',
        #     'Population',
        #     'Administrative Level',
        # ])
        other_cols = [col for col in joined_df.columns.tolist()
                      if col not in front_cols]
        new_cols = front_cols + other_cols
        joined_df = joined_df[new_cols]

        # Rename some columns for display

        joined_df.rename(columns={
            'matched_barangay': 'brgy_linksight',
            'matched_city_municipality': 'municity_linksight',
            'matched_province': 'prov_linksight',
            'code':'psgc',
            'total_score':'confidence_score'
        }, inplace=True)

        # Create matched dataset

        name, _ = os.path.splitext(self.dataset.name)
        self.matched_dataset = Dataset.objects.create(
            name='{}-matched.csv'.format(name),
        )
        file = ContentFile(joined_df.to_csv(index=False))
        self.matched_dataset.file.save(self.matched_dataset.name, file)
        self.save()


class MatchItem(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, editable=False,
                              related_name='items')

    dataset_index = models.IntegerField(editable=False)

    search_tuple = models.CharField(
        max_length=256, unique=True)

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
    chosen = models.BooleanField()

    class Meta:
        ordering = ['dataset_index', '-total_score']
