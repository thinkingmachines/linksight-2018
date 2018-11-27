from functools import partial
from time import time

import pandas as pd

from api.matchers.search_tuple import create_search_tuple, to_index


def is_match(actual, expected):
    if isinstance(expected, str):
        return actual == expected
    else:  # Expect a collection
        return actual in expected


def get_accuracy(answer_key_file, matches, columns):
    answer_key = pd.read_csv(answer_key_file, dtype=str)
    answer_key.set_index(
        answer_key
        .apply(
            partial(create_search_tuple, columns=columns),
            axis=1)
        .apply(to_index),
        inplace=True)

    matched_rows = []
    for match in matches:
        search_tuple = match['search_tuple']
        expected = answer_key.at[search_tuple, 'expected_PSGC']
        actual = match['code']

        if is_match(actual, expected):
            matched_rows.append(search_tuple)

    no_matches = answer_key[~answer_key.index.isin(matched_rows)].to_csv(index=False)

    matches_count = len(matched_rows)
    if matches_count < len(answer_key):
        print("Inputs with no matches: {}\n".format(no_matches))

    print("Found {} correct matches out of {} records\n".format(matches_count, len(answer_key)))

    return matches_count / len(answer_key)


def get_stats(matcher, columns):
    start = time()
    matches = list(matcher.get_matches())
    duration = time() - start
    accuracy = get_accuracy(matcher.dataset_file, matches, columns)

    return {
        'accuracy': accuracy,
        'duration': duration
    }
