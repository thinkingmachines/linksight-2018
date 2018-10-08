import csv
from collections import OrderedDict
from pprint import pprint
from django.test import TestCase
from linksight.api.matchers.ngrams_matcher import NgramsMatcher, REFERENCE_FILE
from tempfile import NamedTemporaryFile
from time import time


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

    def create_matcher(self, dataset):
        return NgramsMatcher(dataset, self.columns)
