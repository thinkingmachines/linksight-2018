'''
This class allows filtering of a dataframe based on whether or not a
dataframe column value contains the target string.
'''

from __future__ import print_function
import pandas as pd


class StringSearcher(object):

    def __init__(self, encoding='utf-8'):
        self.corpus = None
        self.encoding = encoding

    def set_corpus(self, corpus):
        '''
        Set the dataframe to use as a search space.

        corpus: Path to CSV file.
        '''
        self.corpus = pd.read_csv(corpus, encoding=self.encoding)

    def find(self, pattern, on, regex=False):
        '''
        pattern: A string to search for.
        on: name of data frame column to use as search space.
        regex: Set to True to use pattern as a regex.

        self.corpus must be a dataframe with a column whose name is specified
        in the "on" argument.

        Returns a dictionary.
        '''
        search = self.corpus[self.corpus[on].isnull()==False].astype(str)
        found = search[search[on].str.contains(str(pattern),
                                               case=False,
                                               regex=regex)]
        return found.to_dict('list')

if __name__ == '__main__':
    pass
