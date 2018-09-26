import abc


class BaseMatcher(abc.ABC):
    """Returns a dataframe containing the following fields:
        source_barangay
        source_city_municipality
        source_province
        matched_barangay
        matched_barangay_psgc
        matched_barangay_score
        matched_city_municipality
        matched_city_municipality_psgc
        matched_city_municipality_score
        matched_province
        matched_province_psgc
        matched_province_score
        total_score
        match_type

        Requirements:
        match_type is an enum and will have either of the following:
            'no_match': if we don't find a match for all fields
            'near': if there are multiple possible matches or if if there's a partial match
                    Ex: we find the correct province and city, but no match for barangay
            'exact': if it's an exact match for all interlevels

        The matched_* fields can be blank NULL/blank if we didn't find a match for the specific interlevel

        Attributes:
            dataset: the path of the file containing the dataset uploaded by the user
            reference: the path of the file containing the PSGC reference file
    """

    @property
    @abc.abstractmethod
    def reference(self):
        pass

    @abc.abstractmethod
    def get_matches():
        pass
