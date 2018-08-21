import os
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
            ['ILOCOS NORTE', 'ADAMS', 'ADAMS', 'Exact match'],
            ['ILOCOS NORTE', 'ADAMSH', 'ADAMS', 'Near match 1'],
            ['ILOCOS NORTE', 'ADAMS', 'ADAMSH', 'Near match 2'],
            ['ILOCOS NORTEH', 'ADAMS', 'ADAMS', 'Near match 3'],
        ], columns=['Province', 'Municipality', 'Barangay', 'Description'])

        matcher = self.create_matcher(dataset)

        result = matcher.get_matches()

        assert len(result) == 1

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
