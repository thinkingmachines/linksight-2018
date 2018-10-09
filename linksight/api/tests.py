import csv
import linksight.api.profiling as profiling
from collections import OrderedDict
from django.test import TestCase
from linksight.api.matchers.ngrams_matcher import NgramsMatcher
from tempfile import NamedTemporaryFile

CLEAN_FILE = 'data/tests/clean.csv.gz'


def create_test_file(content):
    temp = NamedTemporaryFile(delete=False, mode='w')
    temp.write(content)
    temp.close()
    return temp.name


class LinkSightMatcherTest(TestCase):

    def test_return_possible_matches(self):
        '''
        If there are no exact matches, return the possible matches. The
        possible matches should be sorted with the nearest match at the top.
        '''

        test = '''prov,municity,bgy\nNATIONAL CAPITAL REGION,QUEZON CITY,TEACHERS VILLAGE WST'''
        dataset_path = create_test_file(test)
        matcher = self.create_matcher(dataset_path)
        result = list(matcher.get_matches())

        assert result[0]['matched_barangay'] == 'TEACHERS VILLAGE WEST'
        assert result[1]['matched_barangay'] == 'TEACHERS VILLAGE EAST'

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

        assert result[0]['matched_barangay'] == 'RADIWAN'
        assert result[0]['matched_city_municipality'] == 'IVANA'
        assert result[0]['matched_province'] == 'BATANES'

    def test_cases(self):
        with open('data/tests/test-cases.csv') as f:
            for test_case in csv.DictReader(f):
                self._test_case(test_case)

    def _test_case(self, test_case):

        print('Testing {}...'.format(test_case['name']))

        test = '''prov,municity,bgy\n{},{},{}'''.format(
            test_case['source_pro'],
            test_case['source_mun'],
            test_case['source_bgy']
        )
        dataset_path = create_test_file(test)
        matcher = self.create_matcher(dataset_path)
        result = list(matcher.get_matches())

        expectations = {
            'expected_bgy_psgc': 'code',
            'expected_pro': 'matched_province',
            'expected_mun': 'matched_city_municipality',
            'expected_bgy': 'matched_barangay'
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
        ('bgy', 'bgy'),
        ('municity', 'municity'),
        ('prov', 'prov')
    ])

    def create_matcher(self, dataset, columns=''):
        return NgramsMatcher(dataset, columns or self.columns)

    def test_clean_stats(self):
        matcher = self.create_matcher(CLEAN_FILE)
        (duration, accuracy) = profiling.get_stats(matcher)
        assert accuracy > 0.99
        assert duration < 10
