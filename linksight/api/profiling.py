from time import time


def get_processing_time(matcher):
    print('Time profiling...')
    start = time()
    result = list(matcher.get_matches())
    duration = time() - start
    print('\tClocked in at {}s'.format('%.2f' % duration))
    return (duration, result)
