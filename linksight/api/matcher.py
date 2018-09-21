import operator
import re
import time
from functools import lru_cache, partial
from multiprocessing import Pool
from collections import Counter

import pandas as pd

import jellyfish
from fuzzywuzzy import fuzz

NGRAM_SIZE = 2


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
            # if the location tuple is not yet associated with the ngram, add it to
            # the list of values
            ngram_table[ngram].update([loc])
    return ngram_table


@lru_cache()
def load_reference():
    locations_df = pd.read_csv('data/psgc-locations.csv.gz',
                               dtype={'code': str})
    locations_df['loc_tuple'] = (locations_df['loc_tuple']
                                 .str.split(',')
                                 .apply(tuple))
    locations_df = locations_df.set_index(
        locations_df['loc_tuple'].apply(to_index))
    locations = locations_df.loc_tuple.tolist()
    return locations_df, generate_ngram_table(locations, NGRAM_SIZE)


def to_index(t):
    # FIXME: Improve this
    return ','.join(t)


def create_search_tuple(row, columns):
    locations = row[list(columns.values())].dropna().str.lower()
    locations = locations.str.replace(r'NOT A PROVINCE|CAPITAL|\(|\)|CITY OF|CITY','', case=False)
    locations = locations.str.replace('ñ','n', case=False)
    locations = locations.str.replace(r'BARANGAY|BGY','BGY', case=False)
    locations = locations.str.replace('POBLACION','POB', case=False)
    locations = locations.str.replace(r'[^A-Z0-9\s]', '', case=False).str.strip()
    values = locations.values.tolist()
    lowest_interlevel = None
    # Check lowest interlevel with values to determine lowest interlevel
    for lowest_interlevel in 'bgy', 'municity', 'prov':
        col = columns.get(lowest_interlevel)
        if col and row.dropna().get(col):
            break
    return tuple(values + [lowest_interlevel])


def score_matches(pair, first_item_ratio_weight=.6,
                  other_items_ratio_weight=.4,
                  adm_level_match_multiplier=1.25):
    search_tuple, candidate_tuple = pair

    # split both the search_tuple and candidate_tuple into their name and
    # interlevel components.
    (*search_terms, search_adm) = search_tuple
    (*candidate_terms, candidate_adm, candidate_code) = candidate_tuple

    # split first and remaining terms
    (first_search_term, *other_search_terms) = search_terms
    (first_candidate_term, *other_candidate_terms) = candidate_terms
    
    # check on jw distance ratio between the very first items in searchString
    # and candidateStrings. multiply by 100 since jellyfish returns a decimal
    # between 0 to 1.    

    first_item_ratio = jellyfish.jaro_winkler(first_search_term,
                                              first_candidate_term) * 100

    # if the item has a number in it, improve the score by checking if the numbers 
    # are equivalent with those in the candidate

    # same_digits_multiplier = 1

    # if bool(re.search(first_search_term,r'\d')):
    #     digits_in_first_search_term = "".join(re.findall(r'\d',first_search_term))
    #     digits_in_first_candidate_term = "".join(re.findall(r'\d',first_candidate_term))

    #     same_digits_ratio = fuzz.ratio(digits_in_first_search_term,digits_in_first_candidate_term)

    #     same_digits_multiplier = same_digits_multiplier + (same_digits_ratio/200)

    # check on edit distance ratio between remaining search terms. only do this if there is more than one search term.
    if len(search_terms) > 1:
        other_items_ratio = fuzz.ratio(' '.join(other_search_terms), ' '.join(other_candidate_terms))


    # if a search and the candidate have the same administrative level,
    # this improves the resulting score
    adm_level_match_score = (adm_level_match_multiplier if search_adm in candidate_adm else 1)

    # create a weighted score for the match with weights for each input. 
    # if the search terms have only one term, don't include the similarity score of the other terms.


    if len(search_terms) > 1:
        score = ((
            (first_item_ratio * first_item_ratio_weight + other_items_ratio * other_items_ratio_weight) 
            / adm_level_match_multiplier ) * adm_level_match_score
        )
    else:
        score = ((
            (first_item_ratio * (first_item_ratio_weight+other_items_ratio_weight)) / adm_level_match_multiplier)
            * adm_level_match_score
        )

    return (
        candidate_tuple,
        round(score,2),
        candidate_code
    )


def search_shortlist(search_tuple, shortlist):
    """
    Takes a search tuple and a short list of candidate tuples
    based on common n-grams
    """
    candidate_pairs = [
        (search_tuple, candidate_tuple)
        for candidate_tuple in shortlist
    ]
    # use multiprocessing to run fuzzy matching
    pool = Pool(2)
    results = pool.map(score_matches, candidate_pairs)
    pool.close()
    pool.join()
    return results


def search_reference(search_tuple, ngram_table, nresults):
    # if the search tuple only has one element (bgy, prov, municity), it means
    # it is actually empty. return an empty result
    if len(search_tuple) == 1:
        return search_tuple, tuple()

    # otherwise, if the search tuple has at least one element, turn the first
    # item in the search string into ngrams
    ss_ngrams = list(set(make_ngram(search_tuple[0], NGRAM_SIZE)))


    # create a list of possible matches based on common ngrams between the first
    # items of search tuple and candidates
    possible_matches = []
    for ngram in ss_ngrams:
        # look each n-gram up in the hash list and add the values as
        # possible_matches
        if ngram in ngram_table:
            possible_matches += ngram_table[ngram]

    #let's eliminate any candidates that share fewer than half of the unique n-grams in the search terms. 
    #for example, no need to run fuzzy matching on an candidate with only a single common n-gram with the search terms

    threshold = len(ss_ngrams)/3
    most_possible = [k for k, v in Counter(possible_matches).items() if v >= threshold]


    # calculate similarity scores of search tuples with candidate among
    # possible matches for each unique psgc code, get the match phrase with the
    # highest score:
    scored_shortlist = {
        code: (*result, code)
        for (*result, code) in
        sorted(search_shortlist(search_tuple, most_possible),
               key=operator.itemgetter(1))
    }.values()

    # return top scoring matches
    top_results = sorted(scored_shortlist, key=operator.itemgetter(1),
                         reverse=True)[:nresults]

    return search_tuple, top_results


def get_matches(dataset_df, columns):
    # first, create search tuples for the dataset provided by the user
    dataset_df['search_tuple'] = dataset_df.apply(
        partial(create_search_tuple, columns=columns),
        axis=1)
    dataset_df.drop_duplicates('search_tuple', inplace=True)
    dataset_df.set_index(dataset_df['search_tuple'].apply(to_index),
                         inplace=True)

    # get lowest interlevel selected
    locations_df, ngram_table = load_reference()

    locations_df_find_exact = locations_df.set_index('candidate_terms').rename(columns={
        'bgy':'matched_barangay',
        'municity':'matched_city_municipality',
        'prov':'matched_province'
        })

    # using a more efficient way of finding exact matches first

    exact_matches = dataset_df.join(locations_df_find_exact,how="inner")

    for i, (search_tuple, row) in enumerate(exact_matches.iterrows()):
        print (search_tuple, row.get('matched_barangay'), row.get('matched_city_municipality'))
        yield {
            'dataset_index': i,
            'search_tuple': search_tuple,
            'source_province': row.get(columns.get('prov')),
            'source_city_municipality': row.get(columns.get('municity')),
            'source_barangay': row.get(columns.get('bgy')),
            'match_time': 0,
            'matched_province': row.get('matched_province'),
            'matched_city_municipality': row.get('matched_city_municipality'),
            'matched_barangay': row.get('matched_city_municipality'),
            'code': row.get('code'),
            'total_score': 100,
            'match_type': 'exact',

        }
    
    # then exclude these from those that need fuzzy matching. only process the fuzzy matches next:

    needs_fuzzy_matching = dataset_df.drop(exact_matches.index)

    search_func = partial(search_reference, ngram_table=ngram_table, nresults=5)

    search_tuples = needs_fuzzy_matching.search_tuple.tolist()

    # for each search tuple, find its top matches
    
    result_pairs = map(search_func, search_tuples)

    start_time = time.time()
    for i, (search_tuple, results) in enumerate(result_pairs):
        print (search_tuple)
        #search_tuples = needs_fuzzy_matching.search_tuple.tolist()
        source = needs_fuzzy_matching.loc[to_index(search_tuple)].fillna('')
        match = {
            'dataset_index': len(exact_matches)+i,
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
                match_type = 'near' if len(results) > 1 else 'exact'
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
