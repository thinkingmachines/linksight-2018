import pandas as pd
from django.test import TestCase

from api.models import Match


class ModelsTestCase(TestCase):
    def test_rows_are_not_rearranged_on_export(self):
        match = Match(source_bgy_col="bgy",
                      source_municity_col="mun",
                      source_prov_col="prov")

        data = {"bgy": ["Sabang", "Bulihan", "Sabang"],
                "mun": ["Dasmarinas", "Malolos", "Dasmarinas"],
                "prov": ["Cavite", "Bulacan", "Cavite"]}

        dataset_df = pd.DataFrame(data=data)

        matches = {
            "dataset_index": [0],
            "search_tuple": ["dasmarinas,cavite,municity"],
            "source_province": ["Cavite"],
            "source_city_municipality": ["Dasmarinas"],
            "source_barangay": ["Sabang"],
            "match_time": [0],
            "matched_province": ["Cavite"],
            "matched_city_municipality": ["Dasmarinas"],
            "matched_barangay": [""],
            "code": ["100000000"],
            "total_score": [100],
            "match_type": ["exact"]
        }

        matches_df = pd.DataFrame(data=matches)

        joined_df = match.merge_matches(dataset_df, matches_df)
        expected = ['Sabang', 'Bulihan', 'Sabang']
        actual = joined_df['bgy'].tolist()
        assert expected == actual

    def test_dont_add_unselected_interlevels(self):
        match = Match(source_bgy_col="",
                      source_municity_col="mun",
                      source_prov_col="prov")

        data = {"bgy": ["Sabang"],
                "mun": ["Dasmarinas"],
                "prov": ["Cavite"]}

        dataset_df = pd.DataFrame(data=data)

        matches = {
            "dataset_index": [0],
            "search_tuple": ["dasmarinas,cavite,municity"],
            "source_province": ["Cavite"],
            "source_city_municipality": ["Dasmarinas"],
            "source_barangay": ["Sabang"],
            "match_time": [0],
            "matched_province": ["Cavite"],
            "matched_city_municipality": ["Dasmarinas"],
            "matched_barangay": [""],
            "code": ["100000000"],
            "total_score": [100],
            "match_type": ["exact"]
        }

        matches_df = pd.DataFrame(data=matches)

        joined_df = match.merge_matches(dataset_df, matches_df)
        assert 'bgy_linksight' not in joined_df.columns
