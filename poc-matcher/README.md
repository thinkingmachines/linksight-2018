# POC Matcher

This package is a collection of text cleaner scripts and matcher classes to find
matches for a query string from a corpus of text documents.

### Dependencies
* numpy
* pandas
* nltk
* scipy==0.16.1
* scikit-learn

Required NLTK corpus:
- stopwords
- punkt

Dependencies will be installed during setup.

### Installation

`pip install <git+http://this-repository.git>`

### Usage

1. Create String Searcher and Cosine Matcher objects.

    ```
    from string_searcher import StringSearcher
    from cosine_matcher import CosineMatcher

    str_search = StringSearcher()
    cos_match = CosineMatcher()
    ```

2. Set search space corpus.

    ```
    str_search.set_corpus('path-to-file.csv')
    cos_match.train('path-to-file.csv', train_on='column_name')
    ```

3. Find records with exact, case-insensitive substring matches from a specific column in the corpus.

    ```
    matches = str_search.find('Query String', on='column_name')
    ```

4. Prepare text query.

    ```
    from text_cleaners import clean_tokens, stringify

    clean_query = stringify(clean_tokens('Query String'))
    ```

5. Find top 5 records with the highest cosine similarity score.

    ```
    matches = cos_match.check_matches(clean_query, 5)
    ```

### Contact

Direct all comments and questions to `hello@thinkingmachin.es`.
