import operator
import re
import time
from collections import Counter, OrderedDict
from functools import lru_cache, partial

import jellyfish
import pandas as pd
from fuzzywuzzy import fuzz

from linksight.api.matchers.base_matcher import BaseMatcher
from linksight.api.matchers.search_tuple import create_search_tuple, to_index

NGRAM_SIZE = 3
REFERENCE_FILE = 'data/psgc-locations.csv.gz'


class NgramsMatcher(BaseMatcher):
    reference = REFERENCE_FILE

    @staticmethod
    def make_ngram(string, n):
        """
        Helper function that creates NGrams. Does not include spaces.
        """
        string = re.sub('[^a-zA-Z0-9]+', '', string.lower())
        ngrams = [
            string[i:i + n]
            for i in range(0, len(string) - (n - 1))
        ]
        return list(set(ngrams))

    @staticmethod
    def generate_ngram_table(locations, n):
        # create the dict
        ngram_table = {}
        # for each location tuple
        for loc in locations:
            # get the first item, minus spaces, lowercase
            first_item = re.sub('[^a-zA-Z0-9]+', '', loc[0].lower())
            # for each of these parts, extract the n-grams
            for i in range(0, len(first_item) - (n - 1)):
                ngram = first_item[i:i + n]
                # if the n-gram is not yet in the table, add it as a new
                # key for which value is empty dict
                ngram_table.setdefault(ngram, set())
                # if the location tuple is not yet associated with the ngram,
                # add it to the list of values
                ngram_table[ngram].update([loc])
        return ngram_table

    @lru_cache()
    def load_reference(self):
        locations_df = pd.read_csv(self.reference,
                                   dtype={'code': str})
        locations_df['loc_tuple'] = (locations_df['loc_tuple']
                                     .str.split(',')
                                     .apply(tuple))
        locations_df = locations_df.set_index(
            locations_df['loc_tuple'].apply(to_index))
        locations = locations_df.loc_tuple.tolist()
        return locations_df, self.generate_ngram_table(locations, NGRAM_SIZE)

    @staticmethod
    def score_matches(pair, first_item_ratio_weight=.5,
                      other_items_ratio_weight=.5):
        search_tuple, candidate_tuple = pair

        # split both the search_tuple and candidate_tuple into their name and
        # interlevel components.

        (*search_terms, search_adm) = search_tuple
        (*candidate_terms, candidate_adm, candidate_code) = candidate_tuple

        # split first and remaining terms

        (first_search_term, *other_search_terms) = search_terms
        (first_candidate_term, *other_candidate_terms) = candidate_terms

        # every fuzz match starts with score of 99, then we penalize for differences
        score = 99

        # check on jw distance ratio between the very first items in search terms
        # and candidate terms. multiply by 100 since jellyfish returns a decimal
        # between 0 to 1. inflict a larger penalty for different terms

        first_item_ratio = jellyfish.jaro_winkler(
            first_search_term, first_candidate_term) * 100
        first_item_diff = 100 - first_item_ratio
        score -= first_item_diff * first_item_ratio_weight

        # if a search and the candidate don't have the same administrative level,
        # inflict penalty
        if search_adm != candidate_adm:
            score -= 10

        # penalize missing vs expected higher interlevels
        expected_higher_adm_items = {'bgy':2,'municity':1,'prov':0}[search_adm]
        missing_higher_items = expected_higher_adm_items - len(other_search_terms)
        score -= missing_higher_items * ((other_items_ratio_weight*50)/expected_higher_adm_items)

        # if there are more search terms than candidate terms, inflict a penalty
        if len(search_terms) > len(candidate_terms):
            score -= 30

        # for search terms with higher admin levels provided,
        # score the similarity ratio of each higher admin level with its
        # counterpart in the candidate higher admin levels

        if (len(search_terms) > 1) and (expected_higher_adm_items > 0):
            for i in range(0,len(other_search_terms)):
                try:
                    other_item_ratio = fuzz.ratio(other_search_terms[i],other_candidate_terms[i])
                    score -= (100 - other_item_ratio) * (other_items_ratio_weight/len(other_search_terms))
                except:
                    pass

        return (
            candidate_tuple,
            round(score, 2),
            candidate_code
        )

    def search_shortlist(self, search_tuple, shortlist):
        """
        Takes a search tuple and a short list of candidate tuples
        based on common n-grams
        """
        candidate_pairs = [
            (search_tuple, candidate_tuple)
            for candidate_tuple in shortlist
        ]
        return map(self.score_matches, candidate_pairs)

    def search_reference(self, search_tuple, ngram_table, nresults):
        # if the search tuple only has one element (bgy, prov, municity), it
        # means it is actually empty. return an empty result
        if len(search_tuple) == 1:
            return search_tuple, tuple()

        # otherwise, if the search tuple has at least one element, turn the
        # first item in the search string into ngrams
        ss_ngrams = list(set(self.make_ngram(search_tuple[0], NGRAM_SIZE)))

        # create a list of possible matches based on common ngrams between the
        # first items of search tuple and candidates
        possible_matches = []
        for ngram in ss_ngrams:
            # look each n-gram up in the hash list and add the values as
            # possible_matches
            if ngram in ngram_table:
                possible_matches += ngram_table[ngram]

        # let's eliminate any candidates that share fewer than half of the
        # unique n-grams in the search terms.  for example, no need to run fuzzy
        # matching on an candidate with only a single common n-gram with the
        # search terms

        #threshold = len(ss_ngrams) / 3
        #most_possible = [
        #    k for k, v in Counter(possible_matches).items() if v >= threshold
        #]

        most_possible = set(possible_matches)

        # calculate similarity scores of search tuples with candidate among
        # possible matches for each unique psgc code, get the match phrase with
        # the highest score:
        scored_shortlist = {
            code: (*result, code)
            for (*result, code) in
            sorted(self.search_shortlist(search_tuple, most_possible),
                   key=operator.itemgetter(1))
        }.values()

        # return top scoring matches
        top_results = sorted(scored_shortlist, key=operator.itemgetter(1),
                             reverse=True)[:nresults]

        return search_tuple, top_results

    def get_exact_matches(self, dataset_df, locations_df_find_exact):
        dataset_columns = self.columns

        interlevel_columns = [dataset_columns.get(interlevel) for interlevel in
                              dataset_columns.keys() if dataset_columns.get(interlevel)]
        dataset_df = dataset_df[interlevel_columns].copy()

        dataset_df = self.rename_interlevels(dataset_df)

        exact_matches = dataset_df.join(locations_df_find_exact, how="inner",
                                        lsuffix='_dataset')

        return exact_matches

    def rename_interlevels(self, dataset_df):
        old_columns = self.columns
        new_columns = OrderedDict([
            ('bgy', 'dataset_bgy'),
            ('municity', 'dataset_mun'),
            ('prov', 'dataset_prov'),
        ])

        dataset_df.rename(columns={
            'dataset_{}'.format(old_columns.get('prov')): new_columns.get('prov'),
            'dataset_{}'.format(old_columns.get('municity')): new_columns.get('municity'),
            'dataset_{}'.format(old_columns.get('bgy')): new_columns.get('bgy')
        }, inplace=True)
        return dataset_df

    def get_matches(self):

        columns = self.columns

        dataset_df = pd.read_csv(self.dataset_file)

        # first, create search tuples for the dataset provided by the user
        dataset_df['search_tuple'] = dataset_df.apply(
            partial(create_search_tuple, columns=columns),
            axis=1)
        dataset_df.drop_duplicates('search_tuple', inplace=True)
        dataset_df.set_index(dataset_df['search_tuple'].apply(to_index),
                             inplace=True)

        # get lowest interlevel selected
        locations_df, ngram_table = self.load_reference()

        locations_df_find_exact = (locations_df
                                   .set_index('candidate_terms')
                                   .rename(columns={
                                       'bgy': 'matched_barangay',
                                       'municity': 'matched_city_municipality',
                                       'prov': 'matched_province'
                                   }))

        # using a more efficient way of finding exact matches first
        exact_matches = self.get_exact_matches(dataset_df, locations_df_find_exact)

        for i, (search_tuple, row) in enumerate(exact_matches.iterrows()):
            yield {
                'dataset_index': i,
                'search_tuple': search_tuple,
                'source_province': row.get(columns.get('prov')),
                'source_city_municipality': row.get(columns.get('municity')),
                'source_barangay': row.get(columns.get('bgy')),
                'match_time': 0,
                'matched_province': row.get('matched_province'),
                'matched_city_municipality': row.get('matched_city_municipality'),
                'matched_barangay': row.get('matched_barangay'),
                'code': row.get('code'),
                'total_score': 100,
                'match_type': 'exact',
            }

        # then exclude these from those that need fuzzy matching. only process
        # the fuzzy matches next:
        needs_fuzzy_matching = dataset_df.drop(exact_matches.index)
        search_func = partial(self.search_reference, ngram_table=ngram_table,
                              nresults=5)
        search_tuples = needs_fuzzy_matching.search_tuple.tolist()

        # for each search tuple, find its top matches
        result_pairs = map(search_func, search_tuples)

        start_time = time.time()
        for i, (search_tuple, results) in enumerate(result_pairs):
            source = needs_fuzzy_matching.loc[to_index(search_tuple)].fillna('')
            match = {
                'dataset_index': len(exact_matches) + i,
                'search_tuple': to_index(search_tuple),
                'source_province': source.get(columns.get('prov')),
                'source_city_municipality': source.get(columns.get('municity')),
                'source_barangay': source.get(columns.get('bgy')),
                'match_time': time.time() - start_time,
            }
            start_time = time.time()

            if len(results) > 0:
                for candidate_tuple, score, candidate_code in results:
                    matched = (locations_df
                               .loc[to_index(candidate_tuple)].fillna(''))
                    match_type = 'near'
                    yield {
                        **match,
                        'matched_province': matched['prov'],
                        'matched_city_municipality': matched['municity'],
                        'matched_barangay': matched['bgy'],
                        'code': candidate_code,
                        'total_score': score,
                        'match_type': match_type,
                    }
            else:
                yield {
                    **match,
                    'matched_province': '',
                    'matched_city_municipality': '',
                    'matched_barangay': '',
                    'code': '',
                    'total_score': 0,
                    'match_type': 'no_match',
                }
