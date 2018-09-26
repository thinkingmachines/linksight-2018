import abc


class BaseMatcher(abc.ABC):

    @abc.abstractmethod
    def get_matches():
        """Should be a generator that yields a dictionary containing the following key-value pairs:
        dataset_index: the index of the client dataset row being processed
        search_tuple:
        source_province: the client dataset row's province field. A blank string if not available
        source_city_municipality: the client dataset row's municity field. A blank string if not available
        source_barangay: the client dataset row's barangay field. A blank string if not available
        match_time: how long it took to match the specific row
        matched_province: matched province. A blank string if not available
        matched_city_municipality: matched city/municipality. A blank string if not available
        matched_barangay: matched barangay. A blank string if not available
        code: the matched PSG code
        total_score: matching score
        match_type: an enum and will have either of the following:
            'no_match': if we don't find a match for all fields
            'near': if there are multiple possible matches or if if there's a partial match
                    Ex: we find the correct province and city, but no match for barangay
            'exact': if it's an exact match for all interlevels
        """
        pass
