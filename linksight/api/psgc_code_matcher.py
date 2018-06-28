import re

import numpy as np
import pandas as pd
import recordlinkage as rl

CITY_MATCHING_CODE_SIZE = 4
BGY_MATCHING_CODE_SIZE = 6


def _col_values_to_upper_case(table, fields):
    for field in fields:
        table[field] = table[field].apply(lambda x: x.upper() if not pd.isna(x) else x)
    return table


def _column_to_numeric(df, column):
    df[column] = pd.to_numeric(df[column], errors='coerce')
    return df


def _replace_value_in_col(df, column_name, regex, value=""):
    df[column_name] = df[column_name].apply(lambda x: re.sub(regex, value, x) if not pd.isna(x) else x)
    return df


class PSGCCodeMatcher:

    def __init__(self, psgc, dataset):
        self.psgc = psgc
        self.dataset = dataset

    def process(self):
        self._clean_data()
        return self._collect_matches()

    # TODO: Refactor the replace logic
    def _clean_data(self):
        client_fields = ['Name', 'Barangay', 'Municipality/City', 'Province']
        self.dataset = self.dataset[client_fields]
        self.dataset = _col_values_to_upper_case(self.dataset, client_fields[1:])

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
        self.dataset['Barangay'] = list(self.dataset['Barangay'].replace(standardized_nums, regex=True))
        self.dataset['Municipality/City'] = list(
            self.dataset['Municipality/City'].replace(standardized_nums, regex=True))
        self.dataset['Province'] = list(self.dataset['Province'].replace(standardized_nums, regex=True))

        regex = re.compile(r'BA?RA?N?GA?Y\.?\s')
        self.dataset = _replace_value_in_col(self.dataset, "Barangay", regex)

        regex = re.compile(r"\s\(CAPITAL\)")
        self.dataset = _replace_value_in_col(self.dataset, "Municipality/City", regex)
        self.psgc = _replace_value_in_col(self.psgc, "location", regex)

        regex = re.compile(r"CITY\sOF\s(.*)")
        replacement = lambda m: '{} CITY'.format(m.group(1))
        self.dataset = _replace_value_in_col(self.dataset, "Municipality/City", regex, replacement)
        self.psgc = _replace_value_in_col(self.psgc, "location", regex, replacement)

        regex = re.compile(r"^STO\.?\s(.*)")
        replacement = lambda m: 'SANTO {}'.format(m.group(1))
        self.dataset = _replace_value_in_col(self.dataset, "Barangay", regex, replacement)

    def _collect_matches(self):

        psgc = self.psgc

        higher_level = {}
        if self._dataset_has('Province'):
            prefix = "Matched Province"
            psgc_doc_prov = psgc[(psgc["interlevel"] == 'PROV') | (psgc["interlevel"].isnull())]
            prov_matches = self._generate_potential_matches(prefix=prefix,
                                                            dataset=psgc_doc_prov,
                                                            field='Province')

            prov_matches = self._add_matching_code(prov_matches,
                                                   '{} PSGC Code'.format(prefix),
                                                   CITY_MATCHING_CODE_SIZE)
            higher_level = {
                'table': prov_matches,
                'prefix': prefix,
                'offset': CITY_MATCHING_CODE_SIZE,
            }

        if self._dataset_has('Municipality/City'):
            prefix = 'Matched Mun/City'
            psgc_doc_city = psgc[psgc["interlevel"].isin(['CITY', 'MUN', 'SUBMUN'])]

            city_matches = self._generate_potential_matches(prefix=prefix,
                                                            dataset=psgc_doc_city,
                                                            field="Municipality/City")

            if higher_level:
                city_matches = self._add_matching_code(city_matches,
                                                       '{} PSGC Code'.format(prefix),
                                                       higher_level['offset'])

                partial_merge = self._merge_interlevel_matches(city_matches, higher_level['table'])
                partial_merge['matched'] = False

                partial_merge = self._mark_exact_matches(partial_merge,
                                                         '{} Score'.format(prefix),
                                                         '{} Score'.format(higher_level['prefix']))

                partial_merge = self._add_matching_code(partial_merge,
                                                        '{} PSGC Code'.format(prefix),
                                                        BGY_MATCHING_CODE_SIZE)

                higher_level = {
                    'table': partial_merge,
                    'prefix': prefix,
                    'offset': BGY_MATCHING_CODE_SIZE,
                }
            else:
                city_matches = self._add_matching_code(city_matches,
                                                       '{} PSGC Code'.format(prefix),
                                                       BGY_MATCHING_CODE_SIZE)

                higher_level = {
                    'table': city_matches,
                    'prefix': prefix,
                    'offset': BGY_MATCHING_CODE_SIZE,
                }

        if self._dataset_has('Barangay'):
            prefix = 'Matched Barangay'
            psgc_doc_bgy = psgc[psgc["interlevel"] == 'BGY']

            bgy_matches = self._generate_potential_matches(prefix=prefix,
                                                           dataset=psgc_doc_bgy,
                                                           field="Barangay")

            if higher_level:
                bgy_matches = self._add_matching_code(bgy_matches,
                                                      '{} PSGC Code'.format(prefix),
                                                      higher_level['offset'])

                partial_merge = self._merge_interlevel_matches(bgy_matches, higher_level['table'])
                partial_merge['matched'] = False

                partial_merge = self._mark_exact_matches(partial_merge,
                                                         '{} Score'.format(prefix),
                                                         '{} Score'.format(higher_level['prefix']))

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

        merged = pd.merge(self.dataset, final_merge['table'], how='left', left_index=True, right_on='client_doc_index')
        print(merged[merged['matched']==True])

        return self._add_total_score(merged)

    def _dataset_has(self, field):
        return True if len(self.dataset[self.dataset[field].notna()]) else False

    def _generate_potential_matches(self, prefix, dataset, field):
        """
        Adds the PSGC columns based on the indexes of the passed dataset

        Args:
            prefix: A string to be used as prefix to the column name
            dataset: The dataframe containing PSGC index to be joined to the PSGC dataframe
            field: A string representing the name of the field to be used for matching

        Returns:

        """
        matches = self._get_index_of_matches(field, dataset, 'location')
        matches = self._add_psgc_columns(matches)
        matches = self._rename_interlevel_specific_cols(matches, prefix)
        return matches

    def _get_index_of_matches(self, interlevel, psgc_doc, field):
        """Match the dataset index with the accompanying PSGC index

        The input name is compared to the PSGC reference dataframe on the same inter-level.
        They are scored based on how close the strings are.

        A dataframe is then created with fields containing the indexes of potential matching
        records

        Args:
            interlevel: A string representing the interlevel of the location being matched
            psgc_doc: A dataframe representing the PSGC data
            field: The name of the column that will be used for matching

        Returns:
            A dataframe containing the dataset index, psgc index, and the matching score
        """
        client_doc = self.dataset
        matches_list = []

        indexer = rl.SortedNeighbourhoodIndex(left_on=interlevel,
                                              right_on=field,
                                              window=999)
        pairs = indexer.index(client_doc, psgc_doc)

        comp = rl.Compare()

        comp.exact(interlevel, field)
        comp.string(interlevel, field, label=field)

        # TODO: A better approach for matching cities
        if interlevel == 'Municipality/City':
            regex = re.compile(r"(.*)")
            replacement = lambda m: '{} CITY'.format(m.group(1))
            client_doc['temp'] = list(client_doc[interlevel].str.replace(regex, replacement))
            comp.exact('temp', field, label='temp')
            features = comp.compute(pairs, client_doc, psgc_doc)
            client_doc.drop(columns=['temp'], inplace=True)
        else:
            features = comp.compute(pairs, client_doc, psgc_doc)

        features['score'] = features.sum(axis=1)

        matches = pd.DataFrame(np.array(list(features.index)))
        matches['score'] = list(features['score'])
        matches.columns = ['client_doc_index', 'psgc_code_index', 'score']

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
        columns[columns.index('code')] = '{} PSGC Code'.format(prefix)
        columns[columns.index('score')] = '{} Score'.format(prefix)
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
        df['matching_code'] = list(df[field_name].astype(str).str[:code_offset].astype(int, errors='ignore'))
        df = _column_to_numeric(df, 'matching_code')
        return df

    @staticmethod
    def _merge_interlevel_matches(left_table, right_table):
        merged = pd.merge(left_table,
                          right_table,
                          on=['matching_code', 'client_doc_index'],
                          how='outer',
                          suffixes=('_left', '_right'))
        return merged

    def _mark_exact_matches(self, df, left_score, right_score):
        exact_matches = df[(df[left_score] >= 1) & (df[right_score] >= 1)]
        df.loc[exact_matches.index, 'matched'] = True

        df = self._drop_match_duplicates(df)
        return df

    @staticmethod
    def _drop_match_duplicates(df):
        exact_matches = df[df['matched'] == True]
        df.drop(
            df[(df['client_doc_index'].isin(list(exact_matches['client_doc_index']))) & (df['matched'] == False)].index,
            inplace=True)
        df.drop(columns=['matching_code'], inplace=True)
        return df

    @staticmethod
    def _add_total_score(df):
        regex = re.compile(r'Score', re.IGNORECASE)
        score_columns = list(filter(regex.search, list(df.columns)))

        df['total_score'] = df[score_columns].sum(axis=1)
        df.sort_values(by=['client_doc_index', 'total_score'], ascending=False, inplace=True)
        return df
