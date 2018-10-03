import csv
from django.test import TestCase
from linksight.api.matchers.fuzzywuzzymatcher import FuzzyWuzzyMatcher
from tempfile import NamedTemporaryFile

REFERENCE_FILE = 'data/clean-psgc.csv'


def create_test_file(content):
    temp = NamedTemporaryFile(delete=False, mode='w')
    temp.write(content)
    temp.close()
    return temp.name


class LinkSightMatcherTest(TestCase):

    reference = REFERENCE_FILE

    def test_return_possible_matches(self):
        '''
        If there are no exact matches, return the possible matches. The
        possible matches should be sorted with the nearest match at the top.
        '''

        test = '''pro,mun,bgy\nNATIONAL CAPITAL REGION,QUEZON CITY,TEACHERS VILLAGE WST'''
        dataset_path = create_test_file(test)
        matcher = self.create_matcher(dataset_path)
        result = matcher.get_matches(
            province_col='pro',
            city_municipality_col='mun',
            barangay_col='bgy'
        )

        bgys = result['matched_barangay']
        assert bgys.iloc[0] == 'TEACHERS VILLAGE WEST'
        assert bgys.iloc[1] == 'TEACHERS VILLAGE EAST'
        assert bgys.iloc[2] == 'U.P. VILLAGE'

    def test_cases(self):
        with open('data/test-cases.csv') as f:
            for test_case in csv.DictReader(f):
                self._test_case(test_case)

    def _test_case(self, test_case):

        print('Testing {}...'.format(test_case['name']))

        test = '''pro,mun,bgy\n{},{},{}'''.format(
            test_case['source_pro'],
            test_case['source_mun'],
            test_case['source_bgy']
        )
        dataset_path = create_test_file(test)
        matcher = self.create_matcher(dataset_path)
        result = matcher.get_matches(
            province_col='pro',
            city_municipality_col='mun',
            barangay_col='bgy'
        )

        expectations = {
            'expected_pro_psgc': 'matched_province_psgc',
            'expected_mun_psgc': 'matched_city_municipality_psgc',
            'expected_bgy_psgc': 'matched_barangay_psgc',
            'expected_pro': 'matched_province',
            'expected_mun': 'matched_city_municipality',
            'expected_bgy': 'matched_barangay'
        }

        for expectation, field in expectations.items():
            expected_val = test_case[expectation]
            if expected_val:
                subset = result[field]
                if expected_val == 'MULTIPLE':
                    assert len(subset) > 1
                elif expected_val == 'NONE':
                    assert not len(subset)
                else:
                    assert subset[0] == expected_val

    def create_matcher(self, dataset):
        return FuzzyWuzzyMatcher(
            dataset=dataset,
            reference=self.reference
        )
