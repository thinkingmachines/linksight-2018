import csv
import os
from django.test import TestCase
from linksight.api.fuzzywuzzymatcher import FuzzyWuzzyMatcher
from tempfile import NamedTemporaryFile

REFERENCE_FILE = 'data/clean-psgc.csv'


class LinkSightMatcherTest(TestCase):

    def setUp(self):
        self.reference = REFERENCE_FILE

    def test_exact_match(self):

        test = '''pro,mun,bgy\nILOCOS NORTE,ADAMS,ADAMS'''
        dataset_path = self.create_test_file(test)

        matcher = self.create_matcher(dataset_path)
        result = matcher.get_match_items(
            province_col='pro',
            city_municipality_col='mun',
            barangay_col='bgy'
        )

        os.remove(dataset_path)

        assert len(result) == 1
        assert result['matched_province'].to_string(index=False) == 'ILOCOS NORTE'
        assert result['matched_city_municipality'].to_string(index=False) == 'ADAMS'
        assert result['matched_barangay'].to_string(index=False) == 'ADAMS (POB.)'

    def test_works_with_missing_fields(self):
        '''
        The client should not be required to upload all fields so the matcher
        should be able to provide the most accurate results based on which
        fields are available.
        '''

        test = '''pro,mun,bgy\n,,SOCORRO'''
        dataset_path = self.create_test_file(test)

        matcher = self.create_matcher(dataset_path)
        result = matcher.get_match_items(
            province_col='pro',
            city_municipality_col='mun',
            barangay_col='bgy'
        )

        os.remove(dataset_path)

        assert len(result)

    def test_return_possible_matches(self):
        '''
        If there are no exact matches, return the possible matches. The
        possible matches should be sorted with the nearest match at the top.
        '''

        test = '''pro,mun,bgy\nNATIONAL CAPITAL REGION,QUEZON CITY,TEACHERS VILLAGE WST'''
        dataset_path = self.create_test_file(test)
        matcher = self.create_matcher(dataset_path)
        result = matcher.get_match_items(
            province_col='pro',
            city_municipality_col='mun',
            barangay_col='bgy'
        )

        bgys = result['matched_barangay']
        assert bgys.iloc[0] == 'TEACHERS VILLAGE WEST'
        assert bgys.iloc[1] == 'TEACHERS VILLAGE EAST'
        assert bgys.iloc[2] == 'U.P. VILLAGE'

    def test_infer_higher_interlevels(self):
        '''
        If a higher interlevel has no match or was not provided, the matcher
        should be able to infer it from the lower interlevel match. Example:
        If only Dasmarinas (city) was provided, the resulting dataset should
        include Cavite (province)
        '''

        test = '''pro,mun,bgy\n,DASMARINAS,'''
        dataset_path = self.create_test_file(test)
        matcher = self.create_matcher(dataset_path)
        result = matcher.get_match_items(
            province_col='pro',
            city_municipality_col='mun',
            barangay_col='bgy'
        )

        r = result.iloc[0]
        assert r['matched_city_municipality'] == 'CITY OF DASMARIÑAS'
        assert r['matched_province'] == 'CAVITE'

    def test_edge_cases(self):
        with open('data/edge-cases.csv') as f:
            for edge_case in csv.DictReader(f):
                self._test_edge_case(edge_case)

    def _test_edge_case(self, edge_case):

        print('Testing {}...'.format(edge_case['name']))

        test = '''pro,mun,bgy\n{},{},{}'''.format(
            edge_case['source_pro'],
            edge_case['source_mun'],
            edge_case['source_bgy']
        )
        dataset_path = self.create_test_file(test)
        matcher = self.create_matcher(dataset_path)
        result = matcher.get_match_items(
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
            expected_val = edge_case[expectation]
            if expected_val:
                subset = result[field]
                if expected_val == 'MULTIPLE':
                    assert len(subset) > 1
                elif expected_val == 'NONE':
                    assert not len(subset)
                else:
                    assert subset[0] == expected_val

    @staticmethod
    def create_test_file(content):
        temp = NamedTemporaryFile(delete=False, mode='w')
        temp.write(content)
        temp.close
        return temp.name

    def create_matcher(self, dataset):
        return FuzzyWuzzyMatcher(
            dataset=dataset,
            reference=self.reference
        )
