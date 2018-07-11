import re
import numpy as np
import pandas as pd
import recordlinkage as rl

from fuzzywuzzy import fuzz

PSGC_CODE_LEN = 9
CITY_MATCHING_CODE_SIZE = 4
BGY_MATCHING_CODE_SIZE = 6


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
        merged = self.dataset.copy()

        for interlevel in reversed(self.dataset_interlevels):
            for reference_interlevel in reversed(self.reference_interlevels):
                print("interlevel: {} | reference_interlevel: {}".format(interlevel, reference_interlevel))
                match = self._match(interlevel, reference_interlevel)
                return match

    def _match(self, interlevel, reference_interlevel):
        subset = self._get_subset(0, reference_interlevel)

        indexer = rl.FullIndex()
        pairs = indexer.index(self.dataset, subset)
        compare_cl = rl.Compare()
        pairs = compare_cl.compute(pairs, self.dataset, subset)
        pairs = pd.DataFrame(np.array(list(pairs.index)))
        pairs.columns = ['dataset_index', 'reference_index']

        merged = pd.merge(pairs, self.dataset[[interlevel]],
                          how='left',
                          left_on='dataset_index',
                          right_index=True)

        merged = pd.merge(merged, subset,
                          how='left',
                          left_on='reference_index',
                          right_index=True)

        merged['matched'] = merged.apply(self._get_score, axis=1,
                                         args=[interlevel, self.reference_location_field])
        return merged.loc[merged.matched == True]

    def _get_subset(self, matching_size, reference_interlevel):
        if matching_size == 0:
            return self.reference.loc[self.reference.interlevel == reference_interlevel].copy()

    @staticmethod
    def _get_score(row, source_field, reference_field):
        functions = [fuzz.token_set_ratio]
        for func in functions:
            score = func(row[source_field], row[reference_field])
            if score == 100:
                return True
        return False
