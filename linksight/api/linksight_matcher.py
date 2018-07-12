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

    def get_match(self, dataset):
        self.dataset.fillna("", inplace=True)
        matched_df = self.dataset.copy()

        codes = []
        for interlevel in self.interlevels:
            location = self.dataset.iloc[0][interlevel['dataset_field_name']]

            if location == "":
                continue
            if len(codes) == 0:
                reference_subset = self._get_subset(interlevel)
            else:
                reference_subset = self._get_subset(interlevel, filter_using_code=True, codes=codes)

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

            merged['matched'] = merged.apply(self._get_score, axis=1,
                                             args=[interlevel['dataset_field_name'], 'location'])

            matches = merged.loc[merged.matched == True]
            if len(matches) > 0:
                matches = matches[['dataset_index', 'code', 'location']]
                codes = list(matches['code'])
                matches.columns = ['dataset_index',
                                   'matched_{}_code'.format(interlevel['name']),
                                   'matched_{}'.format(interlevel['name'])]

                matched_df = pd.merge(matched_df, matches,
                                      how='left',
                                      left_index=True,
                                      right_on='dataset_index')
                matched_df.set_index('dataset_index', inplace=True, drop=True)
                matched_df.drop_duplicates(inplace=True)

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
                return True
        return False
