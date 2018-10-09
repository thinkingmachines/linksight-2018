import pandas as pd
from time import time


def get_accuracy(answer_key_file, result):
    # TODO: Use answer key
    answer_key = pd.read_csv(answer_key_file)
    exact = 0
    for i in result:
        if i['match_type'] == 'exact':
            exact += 1
        else:
            print('No exact match found for [{},{},{}]'.format(
                i['source_barangay'],
                i['source_city_municipality'],
                i['source_province']
            ))
    return exact / len(result)


def get_stats(matcher):
    start = time()
    result = list(matcher.get_matches())
    duration = time() - start
    accuracy = get_accuracy(matcher.dataset_file, result)
    return (duration, accuracy)
