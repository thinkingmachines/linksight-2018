import operator
import re
import time
from collections import Counter
from functools import partial
from multiprocessing import Pool

import pandas as pd

import jellyfish
from fuzzywuzzy import fuzz

NGRAM_SIZE = 2


def make_ngram(string, n):
    """
    Helper function that creates NGrams. Does not include spaces.
    """
    string = re.sub("[^a-zA-Z0-9]+","",string.lower())
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
        
        #get the first item, minus spaces, lowercase

        first_item = re.sub('[^a-zA-Z0-9]+', '', loc[0].lower())

        # for each of these parts, extract the n-grams

        for i in range(0, len(first_item) - (n - 1)):

            ngram = first_item[i:i + n]

            # if the n-gram is not yet in the table, add it as a new
            # key for which value is empty dict

            if ngram not in ngram_table.keys():
                    
                ngram_table[ngram] = []

                #ngram_table.setdefault(ngram, set())#.add(tuple(loc))

        #if the location tuple is not yet associated with the ngram, add it to the list of values

        if loc not in ngram_table[ngram]:

            ngram_table[ngram].append(loc)

    return ngram_table


def to_index(t):
    # FIXME: Improve this
    return ','.join(t)


locations_df = pd.read_csv('data/psgc-locations.csv.gz', dtype={'code': str})
locations_df['loc_tuple'] = (locations_df['loc_tuple']
                                 .str.split(',')
                                 .apply(tuple))
locations_df = locations_df.set_index(locations_df['loc_tuple'].apply(to_index))
locations = locations_df.loc_tuple.tolist()
ngram_table = generate_ngram_table(locations, NGRAM_SIZE)

def score_matches(pair, first_item_ratio_weight=.80, other_items_ratio_weight=.15,
                  adm_level_match_weight=.05):
    search_tuple, candidate_tuple = pair

    # split both the search_tuple and candidate_tuple into their name and
    # interlevel components.
    (*search_terms, search_adm) = search_tuple
    (*candidate_terms, candidate_adm, candidate_code) = candidate_tuple

    # split first and remaining terms
    (first_search_term, *other_search_terms) = search_terms

    (first_candidate_term, *other_candidate_terms) = candidate_terms

    # check on jw distance ratio between the very first items in searchString
    # and candidateStrings
    first_item_ratio = jellyfish.jaro_winkler(first_search_term,
                                              first_candidate_term) * 100

    # check on edit distance ratio between remaining search terms
    other_items_ratio = fuzz.ratio(' '.join(other_search_terms),
                                   ' '.join(other_candidate_terms))

    # if a search and the candidate have the same administrative level,
    # this improves the resulting score
    adm_level_match = search_adm == candidate_adm
    adm_level_match_score = (1 if adm_level_match else 0)


    # create a weighted score for the match with weights for each input

    score = (
        first_item_ratio * first_item_ratio_weight +
        other_items_ratio * other_items_ratio_weight +
        adm_level_match_score * adm_level_match_weight
    )
    return (
        candidate_tuple,
        #first_item_ratio,
        #other_items_ratio,
        #adm_level_match,
        round(score,2),
        candidate_code
    )


def search_shortlist(search_tuple, shortlist):

    #takes a search tuple and a short list of candidate tuples based on common n-grams
    
    #from the shortlist, find exact matches first

    exact_match = False

    for candidate_tuple in shortlist:

        exact_match = search_tuple == candidate_tuple[:-1]

        if exact_match:

            # exact matches result in perfect score and a single row returned 
            #with the candidate tuple, total score of 100 and psgc code

            psgc = candidate_tuple[-1]
            
            return [(candidate_tuple, 100, psgc)]

    # if no exact match found, then pair search tuple with each possible candidate tuple

    else:

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

    if len(search_tuple) == 1:

        return search_tuple, tuple()
 

    # turn the first item in the search string into ngrams

    ss_ngrams = list(set(make_ngram(search_tuple[0], NGRAM_SIZE)))

    #create a list of possible matches based on common ngrams between the first items of search tuple and candidates

    possible_matches = []


    for ngram in ss_ngrams:
        
        # look each n-gram up in the hash list and add the values as
        # possible_matches

        if ngram in ngram_table:

            possible_matches += ngram_table[ngram]
    

    #calculate similarity scores of search tuples with candidate among possible matches

    #shortlist_results = pd.DataFrame(search_shortlist(search_tuple,possible_matches)).rename(columns={0:'candidate',1:'score',2:'code'})

    scored_shortlist = {
        code: (*result, code)
        for (*result, code) in
        sorted(search_shortlist(search_tuple, possible_matches),key=operator.itemgetter(1))
    }.values()

    #return top scoring matches

    #top_results = list(shortlist_results.sort_values(by="score",ascending=False).reset_index(drop=True).drop_duplicates(keep="first")[:nresults].to_records())


    top_results = sorted(scored_shortlist, key=operator.itemgetter(1),
                     reverse=True)[:nresults]    


    return search_tuple, top_results


def get_matches(dataset_df, columns):

    #dataset_df.dropna(subset=list(columns.values()),inplace=True)

    def create_search_tuple(row):
        locations = (
            #row[columns]
            row[list(columns.values())]
                .dropna()
                .str.replace('BGY|BRGY|BARANGAY||NOT A PROVINCE|CAPITAL|\(|\)|CITY OF|CITY|', '',
                             case=False)
                .str.replace(r'[^A-Z ]', '', case=False)
                .str.lower()
        )
        values = locations.values.tolist()
        lowest_interlevel = None

        # Check lowest interlevel with values to determine lowest interlevel

        for lowest_interlevel in 'bgy', 'city', 'prov':
            col = columns.get(lowest_interlevel)
            if col and row.dropna().get(col):
                break

        return tuple(values + [lowest_interlevel])

    #first, create search tuples for the dataset provided by the user

    dataset_df['search_tuple'] = dataset_df.apply(create_search_tuple, axis=1)
    dataset_df.drop_duplicates('search_tuple', inplace=True)
    (dataset_df
     .set_index(dataset_df['search_tuple'].apply(to_index),
                inplace=True))

    #get lowest interlevel selected

    start_time = time.time()

    search_func = partial(search_reference, ngram_table=ngram_table, nresults=5)

    search_tuples = dataset_df.search_tuple.tolist()

    #for each search tuple, find its top matches

    print (columns)

    for i, (search_tuple, results) in enumerate(map(search_func, search_tuples)):
        source = dataset_df.loc[to_index(search_tuple)].fillna('')

        
        match = {
            'dataset_index': i,
            'source_province': source.get(columns.get('prov')),
            'source_city_municipality': source.get(columns.get('city')),
            'source_barangay': source.get(columns.get('bgy')),
        }
#        print (match)
        if len(results) > 0:
            for (
                candidate_tuple,
                #first_item_ratio,
                #other_items_ratio,
                #adm_level_match,
                score,
                candidate_code
            ) in results:
                matched = locations_df.loc[to_index(candidate_tuple)].fillna('')
                yield {
                    **match,
                    'matched_province': matched['prov'],
                    'matched_city_municipality': matched['city'],
                    'matched_barangay': matched['bgy'],
                    'code': candidate_code,
                    'total_score': score,
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
