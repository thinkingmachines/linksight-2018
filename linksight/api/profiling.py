from functools import partial
from time import time

import pandas as pd

from linksight.api.matchers.search_tuple import create_search_tuple, to_index


def get_accuracy(answer_key_file, matches, columns):
    answer_key = pd.read_csv(answer_key_file, dtype=str)
    answer_key.set_index(
        answer_key
        .apply(
            partial(create_search_tuple, columns=columns),
            axis=1)
        .apply(to_index),
        inplace=True)

    correct_matches_count = 0
    for match in matches:
        search_tuple = match['search_tuple']
        expected = answer_key.loc[search_tuple]['expected_PSGC']
        actual = match['code']

        if isinstance(expected, str):
            if actual != expected:
                continue
        else:
            if actual not in expected:
                continue

        correct_matches_count += 1

    print("Found {} correct matches out of {} records".format(correct_matches_count, len(answer_key)))

    return correct_matches_count / len(answer_key)


def get_stats(matcher, columns):
    start = time()
    matches = list(matcher.get_matches())
    duration = time() - start
    accuracy = get_accuracy(matcher.dataset_file, matches, columns)

    return {
        'accuracy': accuracy,
        'duration': duration
    }
