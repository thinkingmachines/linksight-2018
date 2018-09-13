import pandas as pd
from django.core.files import File
from django.test import TestCase
from linksight.api.linksight_matcher import LinkSightMatcher
from linksight.api.models import Dataset


class LinkSightMatcherTest(TestCase):

    def setUp(self):
        self.reference = self.get_psgc_df()
        self.interlevels = self.get_interlevels(
            'Province',
            'Municipality',
            'Barangay')

    def test_exact_match(self):

        dataset = pd.DataFrame([
            ['ILOCOS NORTE', 'ADAMS', 'ADAMS'],
        ], columns=['Province', 'Municipality', 'Barangay'])
        matcher = self.create_matcher(dataset)
        result = matcher.get_matches()

        assert len(result) == 3
        assert result.loc[result['interlevel'] == 'Prov']['location'][0] == 'ILOCOS NORTE'
        assert result.loc[result['interlevel'] == 'Mun']['location'][0] == 'ADAMS'
        assert result.loc[result['interlevel'] == 'Bgy']['location'][0] == 'ADAMS (POB.)'

    def test_works_with_missing_fields(self):
        '''
        The client should not be required to upload all fields so the matcher
        should be able to provide the most accurate results based on which
        fields are available.
        '''

        dataset = pd.DataFrame([
            [None, None, 'SOCORRO'],
        ], columns=['Province', 'Municipality', 'Barangay'])
        matcher = self.create_matcher(dataset)
        result = matcher.get_matches()

        assert len(result)

    def test_return_possible_matches(self):
        '''
        If there are no exact matches, return the possible matches. The
        possible matches should be sorted with the nearest match at the top.
        '''

        dataset = pd.DataFrame([
            ['NATIONAL CAPITAL REGION', 'QUEZON CITY', 'TEACHERS VILLAGE WST'],
        ], columns=['Province', 'Municipality', 'Barangay'])
        matcher = self.create_matcher(dataset)
        result = matcher.get_matches()

        bgys = result.loc[result['interlevel'] == 'Bgy']['location']
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

        dataset = pd.DataFrame([
            [None, 'DASMARINAS', None],
        ], columns=['Province', 'Municipality', 'Barangay'])
        matcher = self.create_matcher(dataset)
        result = matcher.get_matches()

        assert result.loc[result['interlevel'] == 'City']['location'][0] == 'CITY OF DASMARIÑAS'
        assert result.loc[result['interlevel'] == 'Prov']['location'][0] == 'CAVITE'

    def create_matcher(self, dataset):
        return LinkSightMatcher(
            dataset=dataset,
            reference=self.reference,
            interlevels=self.interlevels)

    @staticmethod
    def get_psgc_df():

        CITY_MUN_CODE_LEN = 6
        PROV_CODE_LEN = 4
        PSGC_LEN = 9

        psgc_file = open('data/clean-psgc.csv')

        psgc = Dataset.objects.create(name='psgc', file=File(psgc_file))
        with psgc.file.open() as f:
            psgc_df = pd.read_csv(f, dtype={'code': object})

        psgc_df['province_code'] = (psgc_df['code']
                                    .str.slice(stop=PROV_CODE_LEN)
                                    .str.ljust(PSGC_LEN, '0'))
        psgc_df['city_municipality_code'] = (psgc_df['code']
                                             .str.slice(stop=CITY_MUN_CODE_LEN)
                                             .str.ljust(PSGC_LEN, '0'))

        return psgc_df

    @staticmethod
    def get_interlevels(prov_col, mul_col, brgy_col):
        return [
            {
                'name': 'province',
                'dataset_field_name': prov_col,
                'reference_fields': ['Prov', 'Dist']
            },
            {
                'name': 'city_municipality',
                'dataset_field_name': mul_col,
                'reference_fields': ['City', 'Mun', 'SubMun']
            },
            {
                'name': 'barangay',
                'dataset_field_name': brgy_col,
                'reference_fields': ['Bgy']
            },
        ]
