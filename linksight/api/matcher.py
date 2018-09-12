import operator
import re
import time
from collections import Counter
from functools import partial
from multiprocessing import Pool

import pandas as pd

import jellyfish
from fuzzywuzzy import fuzz

NGRAM_SIZE = 4


def make_ngram(string, n):
    """
    Helper function that creates NGrams. Does not include spaces.
    """
    ngrams = [
        string[i:i + n]
        for i in range(0, len(string) - (n - 1))
    ]
    return list(set(ngrams))


def generate_ngram_table(locations, n):
    # create the dict
    ngram_table = {}
    # for each unique location phrase
    for loc in locations:
        # take each unique part in that tuple and extract the n-grams
        for item in loc:
            item = re.sub('[^a-zA-Z0-9]+', '', item.lower())
            # for each of these parts, extract the n-grams
            for i in range(0, len(item) - (n - 1)):
                ngram = item[i:i + n].lower()
                # if the n-gram is not yet in the table, add it as a new
                # key for which value is empty dict
                # else, append the said location name to the values
                # associated with the n-gram
                ngram_table.setdefault(ngram, set()).add(tuple(loc))
    return ngram_table


def score_matches(pair, first_item_ratio_weight=.60, other_items_ratio_weight=.40,
                  adm_level_match_weight=0):
    search_tuple, candidate_tuple = pair

    # split both the search_tuple and candidate_tuple into their name and
    # interlevel components.
    (*search_terms, search_adm) = search_tuple
    (*candidate_terms, candidate_adm, candidate_code) = candidate_tuple

    # split first and remaining terms
    (first_search_term, *other_search_terms) = search_terms
    (first_candidate_term, *other_candidate_terms) = candidate_terms

    # if a search and the candidate have the same administrative level,
    # this improves the resulting score
    adm_level_match = search_adm == candidate_adm
    adm_level_match_score = (1 if adm_level_match else 0)

    # check on jw distance ratio between the very first items in searchString
    # and candidateStrings
    first_item_ratio = jellyfish.jaro_winkler(first_search_term,
                                              first_candidate_term)

    # check on edit distance ratio between remaining search terms
    other_items_ratio = fuzz.ratio(''.join(other_search_terms),
                                   ''.join(other_candidate_terms)) / 100

    # create a weighted score for the match with weights for each input
    total = (
        first_item_ratio * first_item_ratio_weight +
        other_items_ratio * other_items_ratio_weight +
        adm_level_match_score * adm_level_match_weight
    )
    return (
        candidate_tuple,
        first_item_ratio,
        other_items_ratio,
        adm_level_match,
        total,
        candidate_code,
    )


def search_shortlist(search_tuple, shortlist):
    candidate_pairs = []

    for candidate_tuple in shortlist:
        if search_tuple == candidate_tuple[:-1]:
            # exact matches result in perfect score and a single row returned
            return [(candidate_tuple, 1, 1, .3, 1, candidate_tuple[-1])]
        # pair search_tuple with each possible match
        candidate_pairs.append((search_tuple, candidate_tuple))

    # use multiprocessing to run fuzzy matching
    pool = Pool(2)
    results = pool.map(score_matches, candidate_pairs)
    pool.close()
    pool.join()

    return results


def search_reference(search_tuple, ngram_table, nshortlist, nresults):
    possible_matches = []
    # turn the search string into ngrams based on the length of ngrams in the
    # reference table
    ss_ngrams = []
    for item in search_tuple[:-2]:
        ss_ngrams.extend(make_ngram(item, NGRAM_SIZE))
    for ngram in list(set(ss_ngrams)):
        # look each n-gram up in the hash list and add the values as
        # possible_matches
        if ngram in ngram_table:
            possible_matches += ngram_table[ngram]
    # Identify the most likely matches by counting most frequent values, or
    # those have the most ngrams in common with the
    # string inside the search tuple. You can adjust the number of "most likely"
    # matches using the nshortlist argument.
    c = Counter(possible_matches)
    most_possible = [p[0] for p in c.most_common(nshortlist)]
    # apply the wearch_shortlist function to extract exact or top N fuzzy
    # matches. results are deduplicated by code
    shortlist_results = {
        code: (*result, code)
        for (*result, code) in
        search_shortlist(search_tuple, most_possible)
    }.values()
    results = sorted(shortlist_results, key=operator.itemgetter(4),
                     reverse=True)[:nresults]
    return search_tuple, results


def to_index(t):
    # FIXME: Improve this
    return ','.join(t)


def get_matches(dataset_df, columns):
    locations_df = pd.read_csv('data/psgc-locations.csv.gz', dtype={'code': str})
    locations_df['loc_tuple'] = (locations_df['loc_tuple']
                                 .str.split(',')
                                 .apply(tuple))
    (locations_df
     .set_index(locations_df['loc_tuple'].apply(to_index),
                inplace=True))
    locations = locations_df.loc_tuple.tolist()
    ngram_table = generate_ngram_table(locations, NGRAM_SIZE)

    def create_search_tuple(row):
        locations = (
            row[list(columns.values())]
                .dropna()
                .str.replace('BGY|BRGY|BARANGAY||NOT A PROVINCE|CAPITAL|\(|\)|CITY OF|CITY|', '',
                             case=False)
                .str.replace(r'[^A-Z ]', '', case=False)
                .str.lower()
        )
        values = locations.values.tolist()
        lowest_interlevel = None
        # Check lowest interlevel with values to determine common interlevel
        for lowest_interlevel in 'bgy', 'city', 'prov':
            col = columns.get(lowest_interlevel)
            if col and row.dropna().get(col):
                break
        return tuple(values + [lowest_interlevel])

    dataset_df['search_tuple'] = dataset_df.apply(create_search_tuple, axis=1)
    dataset_df.drop_duplicates('search_tuple', inplace=True)
    (dataset_df
     .set_index(dataset_df['search_tuple'].apply(to_index),
                inplace=True))

    start_time = time.time()
    search_func = partial(search_reference, ngram_table=ngram_table,
                          nshortlist=500, nresults=5)
    search_tuples = dataset_df.search_tuple.tolist()
    for i, (search_tuple, results) in enumerate(map(search_func, search_tuples)):
        source = dataset_df.loc[to_index(search_tuple)].fillna('')
        match = {
            'dataset_index': i,
            'source_province': source[columns['prov']],
            'source_city_municipality': source[columns['city']],
            'source_barangay': source[columns['bgy']],
        }
        if len(results) > 0:
            for (
                candidate_tuple,
                first_item_ratio,
                other_items_ratio,
                adm_level_match,
                total,
                candidate_code,
            ) in results:
                matched = locations_df.loc[to_index(candidate_tuple)].fillna('')
                yield {
                    **match,
                    'matched_province': matched['prov'],
                    'matched_city_municipality': matched['city'],
                    'matched_barangay': matched['bgy'],
                    'code': candidate_code,
                    'total_score': total,
                    'match_type': 'near' if len(results) > 1 else 'exact',
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
