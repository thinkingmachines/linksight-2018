'''

This class uses scikit-learn to vectorize a corpus of text and
allow comparison of new documents to the existing corpus matrix

'''

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


class CosineMatcher(object):
    def __init__(self, encoding='utf-8', analyzer='word', ngram_range=(1,1), \
                 min_df = 1, max_df = 0.8, use_idf=True):
        '''
        Defaults

        encoding=utf-8
        min_df = 1 => only include token if it appears in at least 1 document
        max_df = 0.8 => drop the token if it appears in over 80pc of the docs

        We aren't using TfidfVectorizer's built-in tokenizer and stop/stem
        functionality because we have chosen to pre-process that text and will
        be running other types of matching on the stop/stemmed text.

        This code assumes that you have already processed the corpus.

        '''
        self.match_corpus = None
        self.matrix = None
        self.encoding = encoding
        self.vectorizer = TfidfVectorizer(encoding=encoding, analyzer=analyzer,\
            ngram_range=ngram_range, min_df=min_df, max_df=max_df,\
            use_idf=use_idf)


    def train(self, corpus, train_on='training_col'):
        '''
        Fit the training corpus to the TF-IDF Vectorizer.

        corpus: Path to CSV file containing the training corpus.
        train_on: Name of the column in the CSV.
        '''
        df_corpus = pd.read_csv(corpus, encoding=self.encoding)
        self.match_corpus = df_corpus[
            df_corpus[train_on].isnull()==False].reset_index()
        training_corpus = self.match_corpus[train_on].values
        self.matrix = self.vectorizer.fit_transform(training_corpus)


    def check_matches(self, target, n_best):
        '''
        target is a string
        n_best is the number of matches we want returned

        Transforms target query into vector form
        Calculates dot product across tfidf matrix
        Returns a list of the n_best matches for the target
        '''

        if not isinstance(target, unicode) and np.isnan(target):
            target = ''
        vectorized_query = self.vectorizer.transform([target])
        cosine_sim = linear_kernel(vectorized_query, self.matrix).flatten()
        n_best_matches_indices = cosine_sim.argsort()[:-n_best-1:-1]

        best_matches = pd.DataFrame()
        for index in n_best_matches_indices:
            match_values = self.match_corpus.ix[index]
            score = cosine_sim[index]
            match_values['score'] = '{:.2f}'.format(score*100)
            best_matches = best_matches.append(match_values)
        best_matches = best_matches.where((pd.notnull(best_matches)), '')
        return best_matches.to_dict('list')


if __name__ == '__main__':
    pass

