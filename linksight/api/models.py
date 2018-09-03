import json
import os.path
import re
import uuid
from itertools import chain, tee

import pandas as pd

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.db.models import Q
from linksight.api.linksight_matcher import LinkSightMatcher

CITY_MUN_CODE_LEN = 6
PROV_CODE_LEN = 4
PSGC_LEN = 9


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

    def preview(self, n=10):
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

    @staticmethod
    def _mark_matched(df, interlevels):
        df['matched'] = ~df.duplicated('index', keep=False)

        def adjust_matched_field(row):
            if (
                not row['matched_barangay'] and
                not row['matched_city_municipality'] and
                not row['matched_province']
            ):
                return 'no_match'
            for interlevel in interlevels:
                if (
                    row['source_{}'.format(interlevel['name'])] and
                    not row['matched_{}'.format(interlevel['name'])]
                ):
                    return 'near'

            if row['matched']:
                return 'exact'
            else:
                return 'near'

        df['match_type'] = df.apply(adjust_matched_field, axis=1)
        df.drop(columns=['matched'], inplace=True)
        return df

    @staticmethod
    def _add_total_score(df):
        regex = re.compile(r'score', re.IGNORECASE)
        score_columns = list(filter(regex.search, list(df.columns)))

        df['total_score'] = df[score_columns].sum(axis=1)

        return df

    @staticmethod
    def _join_interlevels(matches, dataset, interlevels):
        df = matches.copy().reset_index()
        merged = pd.DataFrame()

        def current_and_prev(iterable):
            current, prev = tee(iterable, 2)
            prev = chain([None], prev)
            return zip(prev, current)

        for prev_interlevel, interlevel in current_and_prev(interlevels):
            interlevel_name = interlevel['name']
            dataset.rename(columns={
                interlevel['dataset_field_name']: 'source_{}'.format(
                    interlevel_name),
            }, inplace=True)
            source_field = 'source_{}'.format(interlevel_name)
            if source_field in dataset:
                dataset[source_field] = dataset[source_field].fillna('')
            else:
                dataset[source_field] = ''

            sub = df[df['interlevel'].isin(interlevel['reference_fields'])].copy()
            sub.drop(columns=['interlevel'], inplace=True)

            updated_column_names = {
                'code': 'matched_{}_psgc'.format(interlevel_name),
                'location': 'matched_{}'.format(interlevel_name),
                'score': 'matched_{}_score'.format(interlevel_name)
            }

            sub.rename(columns=updated_column_names, inplace=True)

            if merged.empty:
                merged = sub
                continue

            prev_interlevel_name = prev_interlevel['name']
            merged = pd.merge(
                sub, merged, how='inner',
                left_on=['index', '{}_code'.format(prev_interlevel_name)],
                right_on=['index', 'matched_{}_psgc'.format(prev_interlevel_name)])

            for column_name, fill_value in (
                ('matched_{}_psgc', 0),
                ('matched_{}', ''),
                ('matched_{}_score', 0),
            ):
                merged[column_name.format(interlevel_name)] = (
                    merged[column_name.format(interlevel_name)].fillna(fill_value)
                )

            merged.drop(
                columns=['{}_code_x'.format(prev_interlevel_name)],
                inplace=True, errors='ignore')
            merged.drop(
                columns=['{}_code_y'.format(prev_interlevel_name)],
                inplace=True, errors='ignore')
            merged.drop(
                columns=['{}_code_x'.format(interlevel_name)],
                inplace=True, errors='ignore')
            merged.drop(
                columns=['{}_code_y'.format(interlevel_name)],
                inplace=True, errors='ignore')

        merged.drop(columns=[
            '{}_code'.format(interlevel['name']) for interlevel in interlevels],
            inplace=True, errors='ignore')

        source_columns = [
            'source_{}'.format(interlevel['name']) for interlevel in interlevels
        ]
        dataset = dataset[source_columns]
        merged = pd.merge(dataset, merged, how='left', left_index=True,
                          right_on='index')

        merged.fillna({
            'matched_barangay': '',
            'matched_city_municipality': '',
            'matched_province': '',
        }, inplace=True)
        return merged

    def generate_match_items(self, **kwargs):
        psgc = Dataset.objects.get(pk=settings.PSGC_DATASET_ID)
        with psgc.file.open() as f:
            psgc_df = pd.read_csv(f, dtype={'code': object})

        with self.dataset.file.open() as f:
            dataset_df = pd.read_csv(f)

        psgc_df['province_code'] = (psgc_df['code']
                                    .str.slice(stop=PROV_CODE_LEN)
                                    .str.ljust(PSGC_LEN, '0'))
        psgc_df['city_municipality_code'] = (psgc_df['code']
                                             .str.slice(stop=CITY_MUN_CODE_LEN)
                                             .str.ljust(PSGC_LEN, '0'))
        interlevels = [
            {
                'name': 'province',
                'dataset_field_name': kwargs.get('province_col'),
                'reference_fields': ['Prov', 'Dist', '']
            },
            {
                'name': 'city_municipality',
                'dataset_field_name': kwargs.get('city_municipality_col'),
                'reference_fields': ['City', 'Mun', 'SubMun']
            },
            {
                'name': 'barangay',
                'dataset_field_name': kwargs.get('barangay_col'),
                'reference_fields': ['Bgy']
            },
        ]

        matcher = LinkSightMatcher(dataset=dataset_df,
                                   reference=psgc_df,
                                   interlevels=interlevels)
        matched_raw = matcher.get_matches()

        matches = self._join_interlevels(matched_raw, dataset_df, interlevels)
        matches = self._mark_matched(matches, interlevels)

        matches.rename(columns={'index': 'dataset_index'}, inplace=True)
        matches = self._add_total_score(matches)

        for _, row in matches.iterrows():
            MatchItem.objects.create(match=self, **row.to_dict(), chosen=False)

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

        matches_df = pd.DataFrame(list(self.items.filter(
            Q(match_type='exact') | Q(chosen=True)
        ).values()))
        matches_df.set_index('dataset_index', inplace=True)

        joined_df = dataset_df.join(matches_df[[
            'matched_barangay',
            'matched_barangay_psgc',
            'matched_city_municipality',
            'matched_city_municipality_psgc',
            'matched_province',
            'matched_province_psgc',
        ]])

        # Get deepest PSGC

        def get_deepest_code(row):
            for field in ['barangay', 'city_municipality', 'province']:
                key = 'matched_{}_psgc'.format(field)
                if row.get(key):
                    return row[key]

        joined_df['PSGC'] = joined_df.apply(
            get_deepest_code, axis=1).astype(str)

        # Merge population

        population = Dataset.objects.get(pk=settings.POPULATION_DATASET_ID)
        with population.file.open() as f:
            population_df = pd.read_csv(f, dtype={'Code': object})

        joined_df = joined_df.merge(population_df, how='left',
                                    left_on='PSGC', right_on='Code',
                                    suffixes=[' (Source)', ''])
        joined_df.drop([
            'Code',
            'matched_barangay_psgc',
            'matched_city_municipality_psgc',
            'matched_province_psgc',
        ], axis='columns', inplace=True)

        # Reorder so matched columns and merged datasets are in front

        front_cols = []
        for source_col, matched_col in (
            (self.barangay_col, 'matched_barangay'),
            (self.city_municipality_col, 'matched_city_municipality'),
            (self.province_col, 'matched_province'),
        ):
            if source_col:
                front_cols.extend((source_col, matched_col))
        front_cols.extend([
            'PSGC',
            'Population',
            'Administrative Level',
        ])
        other_cols = [col for col in joined_df.columns.tolist()
                      if col not in front_cols]
        new_cols = front_cols + other_cols
        joined_df = joined_df[new_cols]

        # Rename some columns for display

        joined_df.rename(columns={
            'matched_barangay': 'Matched Barangay',
            'matched_city_municipality': 'Matched City/Municipality',
            'matched_province': 'Matched Province',
        }, inplace=True)

        # Create matched dataset

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
    matched_barangay_psgc = models.CharField(
        max_length=10, editable=False, null=True)
    matched_barangay_score = models.FloatField(
        editable=False)

    matched_city_municipality = models.CharField(
        max_length=256, editable=False, null=True)
    matched_city_municipality_psgc = models.CharField(
        max_length=10, editable=False, null=True)
    matched_city_municipality_score = models.FloatField(
        editable=False)

    matched_province = models.CharField(
        max_length=256, editable=False, null=True)
    matched_province_psgc = models.CharField(
        max_length=10, editable=False, null=True)
    matched_province_score = models.FloatField(
        editable=False)

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
