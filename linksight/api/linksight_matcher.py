from itertools import dropwhile

import numpy as np
import pandas as pd
import recordlinkage as rl

from fuzzywuzzy import fuzz

CODE_LEN = 9


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
        previous_interlevel = ""
        for interlevel in self.interlevels:
            location = self.dataset.iloc[0][interlevel['dataset_field_name']]

            if location == "":
                matched_df['matched_{}_code'.format(interlevel['name'])] = np.nan
                matched_df['matched_{}'.format(interlevel['name'])] = np.nan
                matched_df['matched_{}_matched'.format(interlevel['name'])] = np.nan
                matched_df['matched_{}_score'.format(interlevel['name'])] = 0
#                previous_interlevel = interlevel
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

                    partial_matches.append(near_matches)
                matches = pd.concat(partial_matches, sort=False)

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

                matched_df["stay"] = matched_df.apply(self._remove_duplicates, axis=1,
                                                      args=(interlevel, previous_interlevel))

                matched_df = matched_df[matched_df["stay"] == True].drop(columns="stay").copy()

                matched_df.set_index('dataset_index', inplace=True, drop=True)
                previous_interlevel = interlevel
            else:
                matched_df['matched_{}_code'.format(interlevel['name'])] = np.nan
                matched_df['matched_{}'.format(interlevel['name'])] = np.nan
                matched_df['matched_{}_matched'.format(interlevel['name'])] = np.nan
                matched_df['matched_{}_score'.format(interlevel['name'])] = 0
#                previous_interlevel = interlevel

        if len(matched_df) == 0:
            mismatch = pd.concat([matched_df, self.dataset], sort=False)
            return mismatch
        else:
            return matched_df

    def _remove_duplicates(self, row, interlevel, previous_interlevel):
        if previous_interlevel == "":
            return True

        current_field = "matched_{}_code".format(interlevel['name'])
        previous_field = "matched_{}_code".format(previous_interlevel['name'])
        code_offset = interlevel['matching_size']
        matching_code = row[current_field][:code_offset].ljust(CODE_LEN, "0")
        if row[previous_field] == matching_code:
            return True
        else:
            return False

    def _get_subset(self, current_interlevel, filter_using_code=False, codes=[]):
        interlevels = dropwhile(lambda x: x != current_interlevel, reversed(self.interlevels))

        if filter_using_code == True:
            for interlevel in interlevels:
                code_field = '{}_code'.format(interlevel['name'])
                subset = self.reference.loc[self.reference[code_field].isin(codes) &
                                            self.reference.interlevel.isin(current_interlevel['reference_fields'])]

                if len(subset) > 0:
                    return subset

        return self.reference.loc[self.reference.interlevel.isin(current_interlevel['reference_fields'])]

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
                                                    args=[interlevel, 'location'],
                                                    result_type='expand')
        return merged

    @staticmethod
    def _drop_mismatches(df):
        if len(df[df['matched'] == 'exact']) > 0:
            return df[df['matched'] == 'exact'].copy()
        else:
            return df[df['matched'] == 'near'].sort_values(by='score', ascending=False).head(5)

    @staticmethod
    def _get_pairs(df1, df2):
        indexer = rl.FullIndex()
        pairs = indexer.index(df1, df2)
        compare_cl = rl.Compare()
        pairs = compare_cl.compute(pairs, df1, df2)
        pairs = pd.DataFrame(np.array(list(pairs.index)))
        return pairs

    @staticmethod
    def _get_score(row, interlevel, reference_field):
        source_field = interlevel['dataset_field_name']

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
