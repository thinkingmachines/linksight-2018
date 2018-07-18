import pandas as pd

from fuzzywuzzy import process

MAX_MATCHES = 10
SCORE_CUTOFF = 80


class LinkSightMatcher:
    def __init__(self, dataset, dataset_index,
                 reference, interlevels):
        self.dataset = dataset
        self.dataset_index = dataset_index
        self.reference = reference
        self.interlevels = interlevels

    def get_matches(self):
        self.dataset.fillna("", inplace=True)
        codes = []
        missing_interlevels = []
        previous_interlevel = ""
        matches = pd.DataFrame()

        for interlevel in self.interlevels:
            location = self.dataset.iloc[0][interlevel["dataset_field_name"]]

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

        matches = self._populate_missing_interlevels(missing_interlevels, matches)
        matches["index"] = self.dataset_index
        matches.set_index("index", drop=True, inplace=True)
        return matches

    def _populate_missing_interlevels(self, interlevels, matches):
        for interlevel in interlevels:
            code_field = "{}_code".format(interlevel["name"])
            if code_field not in self.reference.columns:
                continue

            codes = set(matches[code_field])
            partial_match = self.reference[self.reference['code'].isin(codes)].copy()
            partial_match['score'] = 100
            matches = matches.append(partial_match, sort=False)

        return matches

    def _get_reference_subset(self, interlevel, codes=[], previous_interlevel=""):
        if codes:
            code_field = "{}_code".format(previous_interlevel["name"])
            subset = self.reference.loc[self.reference[code_field].isin(codes) &
                                        self.reference.interlevel.isin(interlevel["reference_fields"])]
            return subset

        return self.reference.loc[self.reference.interlevel.isin(interlevel["reference_fields"])]

    def _get_matches(self, interlevel, reference_subset):
        location = self.dataset.iloc[0][interlevel["dataset_field_name"]]

        choices = {}
        for index, row in reference_subset.reset_index().iterrows():
            if row["location"] not in choices:
                choices[row["location"]] = {}
            choices[row["location"]][row["index"]] = row.to_dict()

        matched_tuples = process.extractBests(location, choices.keys(),
                                              score_cutoff=SCORE_CUTOFF, limit=MAX_MATCHES)

        matches = pd.DataFrame()
        for matched_loc, score in matched_tuples:
            temp = {}
            temp[matched_loc] = choices[matched_loc]
            df = pd.DataFrame.from_dict(temp[matched_loc], orient="index")
            df["score"] = score
            matches = matches.append(df)

        return matches
