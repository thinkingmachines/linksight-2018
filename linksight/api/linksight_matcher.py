import re
import numpy as np
import pandas as pd
import recordlinkage as rl

from fuzzywuzzy import fuzz

PSGC_CODE_LEN = 9


class LinksightMatcher:
    def __init__(self, reference,
                 reference_interlevels,
                 reference_location_field,
                 dataset,
                 dataset_interlevels,
                 interlevels):
        self.reference = reference
        self.reference_interlevels = reference_interlevels
        self.reference_location_field = reference_location_field
        self.dataset = dataset
        self.dataset_interlevels = dataset_interlevels
        self.interlevels = interlevels

    def get_match(self, dataset):
        matched_df = self.dataset.copy()

        for interlevel in self.interlevels:
            reference_subset = self._get_subset(interlevel)

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
            return merged.loc[merged.matched == True]

    def _get_subset(self, interlevel):
        if interlevel['matching_size'] == 0:
            return self.reference.loc[self.reference.interlevel.isin(interlevel['reference_fields'])]

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
