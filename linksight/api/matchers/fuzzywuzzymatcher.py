import pandas as pd
from linksight.api.matcher import Matcher

import re
from itertools import chain, tee
from linksight.api.linksight_matcher import LinkSightMatcher

CITY_MUN_CODE_LEN = 6
PROV_CODE_LEN = 4
PSGC_LEN = 9


class FuzzyWuzzyMatcher(Matcher):
    def get_match_items(self, **kwargs):

        with open(self.reference) as f:
            psgc_df = pd.read_csv(f, dtype={'code': object})

        with open(self.dataset) as f:
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

        return matches

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
