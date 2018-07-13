from itertools import dropwhile

import numpy as np
import pandas as pd
import recordlinkage as rl

from fuzzywuzzy import fuzz
from fuzzywuzzy import process


class LinksightMatcher:
    def __init__(self, reference,
                 reference_location_field,
                 dataset,
                 interlevels):
        self.reference = reference
        self.reference_location_field = reference_location_field
        self.dataset = dataset
        self.interlevels = interlevels

    def get_match(self):
        self.dataset.fillna("", inplace=True)
        matched_df = self.dataset.copy()

        codes = []
        previous_interlevel_name = ""
        for interlevel in self.interlevels:
            location = self.dataset.iloc[0][interlevel['dataset_field_name']]

            if location == "":
                matched_df['matched_{}_code'.format(interlevel['name'])] = np.nan
                matched_df['matched_{}'.format(interlevel['name'])] = np.nan
                matched_df['matched_{}_matched'.format(interlevel['name'])] = np.nan
                matched_df['matched_{}_score'.format(interlevel['name'])] = 0
                continue

            if len(codes) == 0:
                reference_subset = self._get_subset(interlevel)

                merged = self._get_matches(interlevel, reference_subset)
                matches = self._drop_mismatches(merged)
            else:
                partial_matches = []
                for code in codes:
                    reference_subset = self._get_subset(interlevel, filter_using_code=True, codes=[code])
                    merged = self._get_matches(interlevel, reference_subset)
                    near_matches = self._drop_mismatches(merged)

                    if len(near_matches) == 0:
                        matched_df = self._drop_unmatched_row(matched_df, previous_interlevel_name, code)

                    partial_matches.append(near_matches)
                matches = pd.concat(partial_matches)

            if len(matches) > 0:
                matches = matches[['dataset_index', 'code', 'location', 'matched', 'score']]
                codes = list(matches['code'])
                matches.columns = ['dataset_index',
                                   'matched_{}_code'.format(interlevel['name']),
                                   'matched_{}'.format(interlevel['name']),
                                   'matched_{}_matched'.format(interlevel['name']),
                                   'matched_{}_score'.format(interlevel['name'])]

                matched_df = pd.merge(matched_df, matches,
                                      how='left',
                                      left_index=True,
                                      right_on='dataset_index')
                matched_df.set_index('dataset_index', inplace=True, drop=True)
                matched_df.drop_duplicates(inplace=True)
                previous_interlevel_name = interlevel['name']
            else:
                matched_df['matched_{}_code'.format(interlevel['name'])] = np.nan
                matched_df['matched_{}'.format(interlevel['name'])] = np.nan
                matched_df['matched_{}_matched'.format(interlevel['name'])] = np.nan
                matched_df['matched_{}_score'.format(interlevel['name'])] = 0

        if len(matched_df) == 0:
            mismatch = pd.concat([matched_df, self.dataset], sort=False)
            return mismatch
        else:
            return matched_df

    def _get_subset(self, starting_interlevel, filter_using_code=False, codes=[]):
        interlevels = dropwhile(lambda x: x != starting_interlevel, reversed(self.interlevels))

        if filter_using_code == True:
            for interlevel in interlevels:
                code_field = '{}_code'.format(interlevel['name'])
                subset = self.reference.loc[self.reference[code_field].isin(codes) &
                                            self.reference.interlevel.isin(starting_interlevel['reference_fields'])]

                if len(subset) > 0:
                    return subset

        return self.reference.loc[self.reference.interlevel.isin(starting_interlevel['reference_fields'])]

    def _get_matches(self, interlevel, reference_subset):
        pairs = self._get_pairs(self.dataset, reference_subset)
        pairs.columns = ['dataset_index', 'reference_index']

        merged = pd.merge(pairs, self.dataset[[interlevel['dataset_field_name']]],
                          how='left',
                          left_on='dataset_index',
                          right_index=True)

        merged = pd.merge(merged, reference_subset,
                          how='left',
                          left_on='reference_index',
                          right_index=True)

        merged[["matched", "score"]] = merged.apply(self._get_score, axis=1,
                                                    args=[interlevel['dataset_field_name'], 'location'],
                                                    result_type='expand')
        return merged

    @staticmethod
    def _drop_mismatches(df):
        if len(df[df['matched'] == 'exact']) > 0:
            return df[df['matched'] == 'exact'].copy()
        else:
            return df[df['matched'] == 'near'].sort_values(by='score', ascending=False).head(5)

    @staticmethod
    def _drop_unmatched_row(df, previous_interlevel_name, code):
        field_name = "matched_{}_code".format(previous_interlevel_name)
        df.reset_index(inplace=True)
        index_to_drop = df[df[field_name] == code].index[0]
        df.drop(index=[index_to_drop], inplace=True)
        df.set_index('dataset_index', inplace=True, drop=True)
        return df

    @staticmethod
    def _get_pairs(df1, df2):
        indexer = rl.FullIndex()
        pairs = indexer.index(df1, df2)
        compare_cl = rl.Compare()
        pairs = compare_cl.compute(pairs, df1, df2)
        pairs = pd.DataFrame(np.array(list(pairs.index)))
        return pairs

    @staticmethod
    def _get_score(row, source_field, reference_field):
        functions = [fuzz.token_set_ratio]
        for func in functions:
            score = func(row[source_field], row[reference_field])
            if score == 100:
                matched = "exact"
            elif score >= 75:
                matched = "near"
            else:
                matched = "mismatch"
        return [matched, score]
