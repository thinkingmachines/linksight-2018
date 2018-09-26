import abc


class BaseMatcher(abc.ABC):
    def __init__(self, dataset_path, columns):
        """Attributes:
        dataset_path: file path of the dataset to be processed
        columns: ordered dict containing the names of the dataset fields and their corresponding
                 interlevels
        """
        self.dataset_path = dataset_path
        self.columns = columns

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

        Sample return dict for each iteration:
        { 'dataset_index': 12,
          'search_tuple': 'san antonio valley ii,paranaque,bgy',
          'source_province': '',
          'source_city_municipality': 'Paranaque City',
          'source_barangay': 'San Antonio Valley II',
          'match_time': 0.17308688163757324,
          'matched_province': 'QUEZON',
          'matched_city_municipality': 'GUINAYANGAN',
          'matched_barangay': 'SAN ANTONIO',
          'code': '045618037',
          'total_score': 75.09,
          'match_type': 'near'
        }

        """
        pass
