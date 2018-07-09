import re

import numpy as np
import pandas as pd
import recordlinkage as rl

from fuzzywuzzy import fuzz
from fuzzywuzzy import process


RECORD_LINKAGE_ALGORITHMS = ['levenshtein', 'jaro', 'jarowinkler',
                             'damerau_levenshtein', 'qgram', 'cosine']

class LinksightMatcher:
    def __init__(self, reference, reference_interlevels, dataset, dataset_interlevels):
        self.reference = reference
        self.reference_interlevels = reference_interlevels
        self.dataset = dataset
        self.dataset_interlevels = dataset_interlevels

    def get_match(self, dataset):
        for interlevel in reversed(self.dataset_interlevels):
            for reference_interlevel in reversed(self.reference_interlevels):
                print("interlevel: {} | reference_interlevel: {}".format(interlevel, reference_interlevel))
                print(reference_interlevel)
                self._match(interlevel, reference_interlevel)

    def _match(self, interlevel, reference_interlevel):
        subset = self.reference.loc[self.reference.interlevel == reference_interlevel].copy()

        print(self.dataset[interlevel])
        indexer = rl.FullIndex()
        pairs = indexer.index(self.dataset, subset)
        compare_cl = rl.Compare()

        for algorithm in RECORD_LINKAGE_ALGORITHMS:
            compare_cl.string(interlevel, 'location', method=algorithm)

        features = compare_cl.compute(pairs, self.dataset, subset)
        features['score'] = features.sum(axis=1)
        print(features.sort_values(by='score', ascending=False).head())
#        print(features.sort_values(by='0', ascending=False).head())
