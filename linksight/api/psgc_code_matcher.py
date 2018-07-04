import re

import numpy as np
import pandas as pd

import recordlinkage as rl


PSGC_CODE_LEN = 9
CITY_MATCHING_CODE_SIZE = 4
BGY_MATCHING_CODE_SIZE = 6


def _col_values_to_upper_case(table, fields):
    for field in fields:
        table[field] = table[field].apply(lambda x: x.upper() if not pd.isna(x) else x)
    return table


def _replace_value_in_col(df, column_name, regex, value=""):
    df[column_name] = df[column_name].apply(lambda x: re.sub(regex, value, x) if not pd.isna(x) else x)
    return df


class PSGCCodeMatcher:

    def __init__(self, psgc, dataset,
                 barangay_col='Barangay',
                 city_municipality_col='City/Municipality',
                 province_col='Province'):
        self.psgc = psgc
        self.dataset = dataset
        self.barangay_col = barangay_col
        self.city_municipality_col = city_municipality_col
        self.province_col = province_col

    def get_matches(self, max_near_matches):
        self._clean_data()
        matches = self._collect_matches(max_near_matches)
        return matches.sort_values(
            by=['dataset_index', 'total_score'],
            ascending=[True, False],
        )

    # TODO: Refactor the replace logic
    def _clean_data(self):
        self.dataset['source_barangay'] = self.dataset.pop(self.barangay_col)
        self.dataset['source_city_municipality'] = self.dataset.pop(
            self.city_municipality_col)
        self.dataset['source_province'] = self.dataset.pop(self.province_col)

        source_fields = [
            'source_barangay',
            'source_city_municipality',
            'source_province',
        ]
        self.dataset = self.dataset[source_fields]
        self.dataset = _col_values_to_upper_case(self.dataset, source_fields)

        self.psgc = _col_values_to_upper_case(self.psgc, ['location', 'interlevel'])

        uno = re.compile(r'\s(UNO|I)$')
        dos = re.compile(r'\s(DOS|II)$')
        tres = re.compile(r'\s(TRES|III)$')
        kuatro = re.compile(r'\s(KUATRO|IV)$')
        singko = re.compile(r'\s(SINGKO|V)$')
        enye = re.compile(r'Ñ')

        standardized_nums = {
            uno: ' 1',
            dos: ' 2',
            tres: ' 3',
            kuatro: ' 4',
            singko: ' 5',
            enye: 'N',
        }

        self.psgc['location'] = list(self.psgc['location'].replace(standardized_nums, regex=True))
        self.dataset['source_barangay'] = list(self.dataset['source_barangay'].replace(standardized_nums, regex=True))
        self.dataset['source_city_municipality'] = list(
            self.dataset['source_city_municipality'].replace(standardized_nums, regex=True))
        self.dataset['source_province'] = list(self.dataset['source_province'].replace(standardized_nums, regex=True))

        regex = re.compile(r'BA?RA?N?GA?Y\.?\s')
        self.dataset = _replace_value_in_col(self.dataset, 'source_barangay', regex)

        regex = re.compile(r"\s\(CAPITAL\)")
        self.dataset = _replace_value_in_col(self.dataset, 'source_city_municipality', regex)
        self.psgc = _replace_value_in_col(self.psgc, "location", regex)

        regex = re.compile(r"CITY\sOF\s(.*)")
        replacement = lambda m: '{} CITY'.format(m.group(1))
        self.dataset = _replace_value_in_col(self.dataset, 'source_city_municipality', regex, replacement)
        self.psgc = _replace_value_in_col(self.psgc, "location", regex, replacement)

        regex = re.compile(r"^STO\.?\s(.*)")
        replacement = lambda m: 'SANTO {}'.format(m.group(1))
        self.dataset = _replace_value_in_col(self.dataset, 'source_barangay', regex, replacement)

    def _collect_matches(self, max_near_matches=5):

        psgc = self.psgc

        higher_level = {}
        if self._dataset_has('source_province'):
            prefix = 'matched_province'
            psgc_doc_prov = psgc[(psgc["interlevel"] == 'PROV') | (psgc["interlevel"].isnull())]
            prov_matches = self._generate_potential_matches(prefix=prefix,
                                                            psgc_reference_df=psgc_doc_prov,
                                                            field='source_province')

            prov_matches = self._add_matching_code(prov_matches,
                                                   '{}_psgc_code'.format(prefix),
                                                   CITY_MATCHING_CODE_SIZE)
            higher_level = {
                'table': prov_matches,
                'prefix': prefix,
                'offset': CITY_MATCHING_CODE_SIZE,
            }

        if self._dataset_has('source_city_municipality'):
            prefix = 'matched_city_municipality'
            psgc_doc_city = psgc[psgc["interlevel"].isin(['CITY', 'MUN', 'SUBMUN'])]

            city_matches = self._generate_potential_matches(prefix=prefix,
                                                            psgc_reference_df=psgc_doc_city,
                                                            field='source_city_municipality')

            if higher_level:
                city_matches = self._add_matching_code(city_matches,
                                                       '{}_psgc_code'.format(prefix),
                                                       higher_level['offset'])

                partial_merge = self._merge_interlevel_matches(city_matches, higher_level['table'])
                partial_merge['matched'] = False

                partial_merge = self._mark_exact_matches(partial_merge,
                                                         '{}_score'.format(prefix),
                                                         '{}_score'.format(higher_level['prefix']))

                partial_merge = self._fill_parent_interlevel(partial_merge,
                                                             'matched_city_municipality_psgc_code',
                                                             CITY_MATCHING_CODE_SIZE,
                                                             'matched_province')

                partial_merge = self._add_matching_code(partial_merge,
                                                        '{}_psgc_code'.format(prefix),
                                                        BGY_MATCHING_CODE_SIZE)

                higher_level = {
                    'table': partial_merge,
                    'prefix': prefix,
                    'offset': BGY_MATCHING_CODE_SIZE,
                }
            else:
                city_matches = self._add_matching_code(city_matches,
                                                       '{}_psgc_code'.format(prefix),
                                                       BGY_MATCHING_CODE_SIZE)

                higher_level = {
                    'table': city_matches,
                    'prefix': prefix,
                    'offset': BGY_MATCHING_CODE_SIZE,
                }

        if self._dataset_has('source_barangay'):
            prefix = 'matched_barangay'
            psgc_doc_bgy = psgc[psgc["interlevel"] == 'BGY']

            bgy_matches = self._generate_potential_matches(prefix=prefix,
                                                           psgc_reference_df=psgc_doc_bgy,
                                                           field='source_barangay')

            if higher_level:
                bgy_matches = self._add_matching_code(bgy_matches,
                                                      '{}_psgc_code'.format(prefix),
                                                      higher_level['offset'])

                partial_merge = self._merge_interlevel_matches(bgy_matches, higher_level['table'])
                partial_merge['matched'] = False

                partial_merge = self._mark_exact_matches(partial_merge,
                                                         '{}_score'.format(prefix),
                                                         '{}_score'.format(higher_level['prefix']))

                final_merge = {
                    'table': partial_merge,
                    'prefix': prefix
                }
            else:
                final_merge = {
                    'table': bgy_matches,
                    'prefix': prefix
                }

        else:
            final_merge = higher_level

        merged = pd.merge(self.dataset, final_merge['table'], how='left', left_index=True, right_on='dataset_index')
        scored = self._add_total_score(merged)
        return scored.groupby(['dataset_index']).head(max_near_matches)

    def _dataset_has(self, field):
        return True if len(self.dataset[self.dataset[field].notna()]) else False

    def _generate_potential_matches(self, prefix, psgc_reference_df, field):
        """
        Adds the PSGC columns based on the indexes of the passed dataset

        Args:
            prefix: A string to be used as prefix to the column name
            psgc_reference_df: The dataframe containing PSGC index to be joined to the PSGC dataframe
            field: A string representing the name of the field to be used for matching

        Returns:

        """
        matches = self._get_index_of_matches(field, psgc_reference_df, 'location')
        matches = self._add_psgc_columns(matches)
        matches = self._rename_interlevel_specific_cols(matches, prefix)
        return matches

    def _get_index_of_matches(self, interlevel, psgc_reference_df, field):
        """Match the dataset index with the accompanying PSGC index

        The input name is compared to the PSGC reference dataframe on the same inter-level.
        They are scored based on how close the strings are.

        A dataframe is then created with fields containing the indexes of potential matching
        records

        Args:
            interlevel: A string representing the interlevel of the location being matched
            psgc_reference_df: A dataframe representing the PSGC data
            field: The name of the column that will be used for matching

        Returns:
            A dataframe containing the dataset index, psgc index, and the matching score
        """
        dataset = self.dataset
        matches_list = []

        indexer = rl.SortedNeighbourhoodIndex(left_on=interlevel,
                                              right_on=field,
                                              window=999)
        pairs = indexer.index(dataset, psgc_reference_df)

        comp = rl.Compare()

        comp.exact(interlevel, field)
        comp.string(interlevel, field, label=field)

        # TODO: A better approach for matching cities
        if interlevel == 'source_city_municipality':
            regex = re.compile(r"(.*)")
            replacement = lambda m: '{} CITY'.format(m.group(1))
            dataset['temp'] = list(dataset[interlevel].str.replace(regex, replacement))
            comp.exact('temp', field, label='temp')
            features = comp.compute(pairs, dataset, psgc_reference_df)
            dataset.drop(columns=['temp'], inplace=True)
        else:
            features = comp.compute(pairs, dataset, psgc_reference_df)

        features['score'] = features.sum(axis=1)

        matches = pd.DataFrame(np.array(list(features.index)))
        matches['score'] = list(features['score'])
        matches.columns = ['dataset_index', 'psgc_code_index', 'score']

        matches_list.append(matches[matches['score'] > 0])

        combined = pd.concat(matches_list)
        return combined

    def _add_psgc_columns(self, table):
        psgc_doc = self.psgc
        table = pd.merge(table,
                         psgc_doc[['location', 'code']],
                         how='left',
                         left_on='psgc_code_index',
                         right_index=True)
        table.drop(columns=['psgc_code_index'], inplace=True)
        return table

    @staticmethod
    def _rename_interlevel_specific_cols(table, prefix):
        columns = list(table.columns)
        columns[columns.index('location')] = prefix
        columns[columns.index('code')] = '{}_psgc_code'.format(prefix)
        columns[columns.index('score')] = '{}_score'.format(prefix)
        table.columns = columns
        return table

    @staticmethod
    def _add_matching_code(df, field_name, code_offset):
        """
        Adds a column containing the sliced PSGC code based on the offset

        Args:
            df: The dataframe to be changed
            field_name: A string representing the name of the field that will be used to generate the matching code
            code_offset: An integer that represents how many digits we need from the PSGC code

        Returns:
            A dataframe containing the matching code

        """
        df['matching_code'] = list(df[field_name].astype(str).str[:code_offset])
        return df

    @staticmethod
    def _merge_interlevel_matches(left_table, right_table):
        merged = pd.merge(left_table,
                          right_table,
                          on=['matching_code', 'dataset_index'],
                          how='outer',
                          suffixes=('_left', '_right'))
        return merged

    def _mark_exact_matches(self, df, left_score, right_score):
        exact_matches = df[(df[left_score] >= 1) & (df[right_score] >= 1)]
        df.loc[exact_matches.index, 'matched'] = True

        df = self._drop_match_duplicates(df)
        return df

    def _fill_parent_interlevel(self, df, psgc_code_field, code_offset, field_to_populate):
        df['matching_code'] = df[psgc_code_field].str.slice(start=code_offset).str.ljust(PSGC_CODE_LEN, '0')

        merged = pd.merge(df, self.psgc, how='left', left_on='matching_code', right_on='code')
        merged.loc[merged[field_to_populate].isnull(), field_to_populate] = merged["location"]
        merged.drop(columns=["location", "code", "interlevel"], inplace=True)
        return merged

    @staticmethod
    def _drop_match_duplicates(df):
        exact_matches = df[df['matched'] == True]
        df.drop(
            df[(df['dataset_index'].isin(list(exact_matches['dataset_index']))) & (df['matched'] == False)].index,
            inplace=True)
        df.drop(columns=['matching_code'], inplace=True)
        return df

    @staticmethod
    def _add_total_score(df):
        regex = re.compile(r'score', re.IGNORECASE)
        score_columns = list(filter(regex.search, list(df.columns)))

        df['total_score'] = df[score_columns].sum(axis=1)
        df.sort_values(by=['dataset_index', 'total_score'], ascending=False, inplace=True)
        return df
