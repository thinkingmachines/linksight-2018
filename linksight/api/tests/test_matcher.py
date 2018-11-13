import csv
from collections import OrderedDict
from tempfile import NamedTemporaryFile

import numpy as np
from django.test import TestCase

from linksight.api import profiling
from linksight.api.matchers.ngrams_matcher import NgramsMatcher

CLEAN_FILE = 'data/tests/clean.csv'
MESSY_FILE = 'data/tests/messy.csv'


def create_test_file(content):
    temp = NamedTemporaryFile(delete=False, mode='w')
    temp.write(content)
    temp.close()
    return temp.name


class MatcherTestBase():

    def test_return_possible_matches(self):
        '''
        If there are no exact matches, return the possible matches. The
        possible matches should be sorted with the nearest match at the top.
        '''

        test = '''input_prov,input_mun,input_bgy\nNATIONAL CAPITAL REGION,QUEZON CITY,TEACHERS VILLAGE WST'''
        dataset_path = create_test_file(test)
        matcher = self.create_matcher(dataset_path)
        result = list(matcher.get_matches())

        assert result[0]['code'] == '137404123'
        assert result[1]['code'] == '137404122'

    def test_linksight_column_name_clash(self):
        '''
        If the dataset contains field names that are in conflict with the field names of the
        matcher's output, it should still be able to return the correct values mapped to the
        correct fields
        '''
        header = ','.join(['matched_barangay',
                           'matched_city_municipality',
                           'matched_province'])
        body = '''Radiwan,Ivana,Batanes'''

        test = "{}\n{}".format(header, body)
        dataset_path = create_test_file(test)

        columns = OrderedDict([
            ('bgy', 'matched_barangay'),
            ('municity', 'matched_city_municipality'),
            ('prov', 'matched_province')
        ])
        matcher = self.create_matcher(dataset_path, columns=columns)
        result = list(matcher.get_matches())

        assert result[0]['matched_barangay'].upper() == 'RADIWAN'
        assert result[0]['matched_city_municipality'].upper() == 'IVANA'
        assert result[0]['matched_province'].upper() == 'BATANES'

    def test_nan_values_on_results(self):
        '''
        The results should not contain 'nan'
        '''
        header = ','.join(['input_bgy',
                           'input_mun',
                           'input_prov'])
        body = ''',Ivana,Batanes'''

        test = "{}\n{}".format(header, body)
        dataset_path = create_test_file(test)

        matcher = self.create_matcher(dataset_path)
        result = list(matcher.get_matches())

        assert np.nan not in list(result[0].values())

    def test_cases(self):
        with open('data/tests/test-cases.csv') as f:
            for test_case in csv.DictReader(f):
                self._test_case(test_case)

    def _test_case(self, test_case):

        print('Testing {}...'.format(test_case['name']))

        test = '''input_prov,input_mun,input_bgy\n{},{},{}'''.format(
            test_case['source_pro'],
            test_case['source_mun'],
            test_case['source_bgy']
        )
        dataset_path = create_test_file(test)
        matcher = self.create_matcher(dataset_path)
        result = list(matcher.get_matches())

        expectations = {
            'expected_bgy_psgc': 'code',
        }

        for expectation, field in expectations.items():
            expected_val = test_case[expectation]
            if expected_val:
                if expected_val == 'MULTIPLE':
                    assert len(result) > 1
                elif expected_val == 'NONE':
                    assert not len(result)
                else:
                    assert expected_val in map(lambda r: r[field], result)

    columns = OrderedDict([
        ('bgy', 'input_bgy'),
        ('municity', 'input_mun'),
        ('prov', 'input_prov')
    ])

    def create_matcher(self, dataset, columns=None):
        return self.matcher_class(dataset, columns or self.columns)

    def test_clean_stats(self):
        matcher = self.create_matcher(CLEAN_FILE)
        stats = profiling.get_stats(matcher, self.columns)
        accuracy = stats['accuracy']
        duration = stats['duration']
        print('Clean:')
        print('\tDuration: {}'.format('%.2f' % duration))
        print('\tAccuracy: {}'.format('%.2f' % accuracy))
        assert accuracy > 0.85
        assert duration < 15

    def test_messy_stats(self):
        matcher = self.create_matcher(MESSY_FILE)
        stats = profiling.get_stats(matcher, self.columns)
        accuracy = stats['accuracy']
        duration = stats['duration']
        print('Messy:')
        print('\tDuration: {}'.format('%.2f' % duration))
        print('\tAccuracy: {}'.format('%.2f' % accuracy))
        assert accuracy > 0.85
        assert duration < 250


class NgramsMatcherTest(MatcherTestBase, TestCase):
    matcher_class = NgramsMatcher
