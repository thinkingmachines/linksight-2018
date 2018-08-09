from itertools import chain, islice, tee

import numpy as np
import pandas as pd
from fuzzywuzzy import process

MAX_MATCHES = 7
MAX_SCORE_DIFF = 9
SCORE_CUTOFF = 80


def previous_and_next(iterable):
    prev, current, nxt = tee(iterable, 3)
    prev = chain([None], prev)
    nxt = chain(islice(nxt, 1, None), [None])
    return zip(prev, current, nxt)


class LinkSightMatcher:
    """Returns a dataframe containing near and exact address matches

    Attributes:
        dataset: pandas dataframe row containing the barangay, city_municipality, and province field
        dataset_index: the index of the dataset being processed
        reference: pandas dataframe containing the reference codes based on the location
        interlevels: dict containing interlevel information:
            name: interlevel name
            dataset_field_name: the dataset's column name corresponding to the interlevel
            reference_fields: list of interlevel values from the reference dataframe that are
                              considered as part of the interlevel
    """
    def __init__(self, dataset, dataset_index,
                 reference, interlevels):
        self.dataset = dataset
        self.dataset_index = dataset_index
        self.reference = reference
        self.interlevels = interlevels

    def get_matches_via_sql(self):
        from linksight.api.models import Reference

        self.dataset.fillna("", inplace=True)

        # TODO dynamically build the query bsed on available fields
        query = self._generate_query()
        matches = Reference.objects.raw(query)

        matches_df = pd.DataFrame()
        for match in matches:
            matches_df = matches_df.append(match.preview())
        return matches_df

    def _generate_query(self):
        interlevels = [interlevel for interlevel in self.interlevels if interlevel['dataset_field_name']]

        query = ""
        for prev, interlevel, nxt in previous_and_next(interlevels):

            if not prev:
                query = ''.join(self._generate_base_query(interlevel))
            elif not nxt:
                (base_query, interlevel_condition, sort_condition) = self._generate_base_query(interlevel, base=True)
                internal_query = 'and {}_code in ({}) '.format(prev['name'], query)
                query = base_query + interlevel_condition + internal_query + sort_condition
            else:
                (base_query, interlevel_condition, sort_condition) = self._generate_base_query(interlevel)
                internal_query = 'and {}_code in ({}) '.format(prev['name'], query)
                query = base_query + interlevel_condition + internal_query + sort_condition
        return query

    def _generate_base_query(self, interlevel, base=False):
        base_query = "select code from api_reference "
        location = self.dataset.iloc[0][interlevel['dataset_field_name']].replace("'", '')
        if base:
            base_query = "select * from api_reference "
        interlevel_condition = "where interlevel in ({}) ".format(', '.join("'{0}'".format(w) for w in interlevel['reference_fields']))
        sort_condition = "order by similarity('{}', location) desc limit 10 ".format(location)
        return base_query, interlevel_condition, sort_condition

    def get_matches(self):
        """Gets potential address matches based on the a dataset row

        :returns: a dataframe containing all of the matches in all interlevels in the following format:
        | code | interlevel | location | province_code | city_municipality_code | score
        """

        self.dataset.fillna("", inplace=True)
        codes = []
        missing_interlevels = []
        previous_interlevel = ""
        matches = pd.DataFrame()

        for interlevel in self.interlevels:
            field_name = interlevel["dataset_field_name"]
            if not field_name:
                missing_interlevels.append(interlevel)
                continue

            location = self.dataset.iloc[0][field_name]

            if location == "":
                missing_interlevels.append(interlevel)
                continue

            subset = self._get_reference_subset(interlevel, codes=codes, previous_interlevel=previous_interlevel)
            partial_matches = self._get_matches(interlevel, subset)

            if len(partial_matches) == 0:
                missing_interlevels.append(interlevel)
                continue

            codes = list(partial_matches["code"])
            matches = matches.append(partial_matches)
            previous_interlevel = interlevel

        if matches.empty:
            return matches
        matches = pd.merge(matches[['code', 'score']].copy(),
                           self.reference[self.reference.original == True].copy(),
                           how='inner', on='code')
        matches = self._populate_missing_interlevels(missing_interlevels, matches)
        matches["index"] = self.dataset_index
        matches.set_index("index", drop=True, inplace=True)
        matches.drop(columns=['original'], inplace=True)

        return matches

    def _populate_missing_interlevels(self, missing_interlevels, matches):
        """Extracts missing higher-interlevel rows based on the matched lower-level ones. If the
        lowest level is missing, the method will add empty dataframes with higher-level interlevel
        codes populated so we can join them later

        :param missing_interlevels: list of unmatched interlevels
        :param matches: the dataframe containing the matches
        :returns: a Pandas dataframe
        """
        for missing_interlevel in missing_interlevels:
            code_field = "{}_code".format(missing_interlevel["name"])

            if code_field not in self.reference.columns:
                matches = self._create_empty_rows(missing_interlevel, matches)
                continue

            codes = set(matches[code_field])
            partial_match = self.reference.loc[self.reference['code'].isin(codes) &
                                               self.reference.interlevel.isin(missing_interlevel["reference_fields"])].copy()

            if partial_match.empty:
                matches = self._create_empty_rows(missing_interlevel, matches)
                continue

            partial_match['score'] = 100
            matches = matches.append(partial_match, sort=False)

        return matches

    def _create_empty_rows(self, missing_interlevel, matches):
        """Appends rows to the dataframe. These rows will be a copy of the matched dataframe but
        with the interlevel changed to match the missing interlevel. The location will be empty.
        The city_municipality_code and province_code will be the same as the matched one so we can
        join them later in the process

        :param missing_interlevel: dict containing the interlevel details
        :param matches: the dataframe containing the matches
        :returns: a pandas dataframe

        """
        partial_match = matches.copy()
        partial_match["interlevel"] = missing_interlevel["reference_fields"][0]
        partial_match["location"] = np.nan
        partial_match.drop_duplicates(["code"], inplace=True)
        partial_match["score"] = 0

        matches = matches.append(partial_match, sort=False)
        return matches.copy()

    def _get_reference_subset(self, interlevel, codes=[], previous_interlevel=""):
        """Returns a subset of the reference dataset based on the current interlevel and the results
        of the previous interlevel match attempt

        :param interlevel: the dict containing info on the interlevel being processed
        :param codes: the list containing the last successfully-matched codes
        :param previous_interlevel: the dict containing info the last processed interleel
        :returns: a pandas dataframe
        """
        if codes:
            code_field = "{}_code".format(previous_interlevel["name"])
            subset = self.reference.loc[self.reference[code_field].isin(codes) &
                                        self.reference.interlevel.isin(interlevel["reference_fields"])]
            return subset

        return self.reference.loc[self.reference.interlevel.isin(interlevel["reference_fields"])]

    def _get_matches(self, interlevel, reference_subset):
        """Returns a dataframe containing matches found on a certain interlevel in the following format:
        | code | interlevel | location | province_code | city_municipality_code | score

        :param interlevel: the dict containing intelevel information
        :param reference_subset: the dataframe containing a subset of the reference dataframe where
                                 the matches will be based on
        :returns: a Pandas dataframe
        """

        location = self.dataset.iloc[0][interlevel["dataset_field_name"]]

        choices = {}
        for index, row in reference_subset.reset_index().iterrows():
            if row["location"] not in choices:
                choices[row["location"]] = {}
            choices[row["location"]][row["index"]] = row.to_dict()

        matched_tuples = process.extractBests(location, choices.keys(),
                                              score_cutoff=SCORE_CUTOFF, limit=MAX_MATCHES)

        prev_score = 0
        matches = pd.DataFrame()
        for matched_loc, score in matched_tuples:
            if prev_score and (prev_score - score) >= MAX_SCORE_DIFF:
                break
            prev_score = score
            temp = {}
            temp[matched_loc] = choices[matched_loc]
            df = pd.DataFrame.from_dict(temp[matched_loc], orient="index")
            df["score"] = score
            matches = matches.append(df)

        if len(matches) and len(matches[matches["score"] == 100]):
            return matches[matches["score"] == 100].copy()
        else:
            return matches
