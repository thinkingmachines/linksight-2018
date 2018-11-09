# Changelog

## Sprint 8 / 2018-11-09
- Document iMatch API
- Move PSGC reference file to a separate repo
- Fix bugs in exported dataset

## Sprint 7 / 2018-10-26
- Tests improvement
- Run matchers in Celery workers
- New matcher: iMatch
- Migrate production to new deployment system
- Expose API to public

## Sprint 6 / 2018-10-12
- Setup continuous integration
- Create a list of all testing cases

## Sprint 5 / 2018-10-05
- Start this changelog
- Automate staging server deployment

## Sprint 4 / 2018-09-28
- Standardize matchers
- Create staging server
- Upload dataset files to GCS
- Improve reference file
- Switch to Google sign-in tied to an approve emails Google sheet
- Add demo dataset

## Sprint 3 / 2018-09-21
- Improve user experience
  - CTA for home is now for login/register
  - Move upload to a login-required step
  - Add sidebar on each step with instructions
  - Update match checking step layout
  - Update export step layout
  - Add feedback page
- New matching algorithm:

    **NGram Algorithm**

    This search algorithm receives a combination of up to three strings–representing any complete set of subset of
    barangay, city or municipality, and province names–and finds either its exact match or top N closest matches from
    within a reference file of administrative territories in the Philippine Standard Geographic Code. The components
    of the search terms and the candidate terms must be sorted from lowest to highest administrative hierarchy.

    The first step is to find exact matches for each set of search terms. We get these by directly joining the table
    of search items with the reference file, using search and candidate terms as the join key. Exact matches are
    assigned a confidence score of 100 and only one row is returned. Only items that escape this direct join need
    to undergo fuzzy matching.

    The fuzzy matching process begins by narrowing down a search term’s list of candidate matches to those with which
    it shares at least one trigram at the lowest level component. A trigram is a contiguous sequence of three
    characters. For example, the first item in “Pipias, Bacarra” contains the trigrams ‘pip’, ‘ipi’, ‘pia’, and ‘ias’.
    Its candidate matches would therefore only include include locations whose first item also contains at least one
    of these trigrams.

    After the list of candidates is narrowed, we score the similarity between the search term and each candidate.
    The initial similarity score starts at 99 and is subsequently penalized based on various rules, in order of weight:
    - Dissimilarity or inverse Jaro-Winkler ratio between lowest administrative level in the search and candidate terms
    - Dissimilarity or inverse Levenshtein ratio between common available higher administrative level items in search
      and candidate terms
    - Absence of expected number of higher administrative level items in search terms
    - Mismatched administrative level between search and candidate

    After the similarity score between each set of search terms and all its candidates are calculated,
    the top five (5) results are returned.


## Sprint 2 / 2018-09-14
- Add registration
- Initial tests
- Add file validation
- Matcher fixes
- UI copy changes
- Add Sentry error tracking
- Append matched columns next to source columns
- Remove external datasets
- Add disclaimer on keeping data
- Allow empty source location columns
- Handle error responses
- Color additional columns
- Add Google Analytics
- Add topbar "Alpha software" disclaimer

## Sprint 1 (Prototype)
- Initial UI and matcher

    The initial matcher utilizes [`fuzzywuzzy`](https://github.com/seatgeek/fuzzywuzzy). Each row of the dataset is
    matched to the PSGC reference file per available interlevel following this process:
    - Check for exact string/substring match. If one or more is found, go to the next interlevel
    - If no exact match is found, then use `fuzzywuzzy` to find the top ten likely candidates. The likely candidates
      are chosen by score. There is a minimum score set and if the results scored below that, then no match will
      be returned
    - After finding match candidates, the matcher will proceed to the next interlevel and do the same logic but
      only match it against a subset of the reference file, filtered by the found matches

    Each interlevel match is represented as a row in the match results with the index being the same as the dataset's
    row number being matched. A sample result for one dataset row is below:

    index | code | interlevel | location | province_code | city_municipality_code | score |
    | --- | ---  | ---------- | -------- | ------------- | ---------------------- | ----- |
    | 0 | 042106010 | Bgy | Barangay Sabang | 042100000 | 042106000 | 100 |
    | 0 | 042106000 | City | City of Dasmariñas | 042100000 | 042106000 | 100 |
    | 0 | 042100000 | City | Province of Cavite | 042100000 | 042100000 | 100 |

    This will then be joined based on the `city_municipality_code` and `province_code` fields resulting to a single
    candidate match row. The match type be computed based on the score with perfect scores marked as `exact`.
    Dataset rows with no match are marked as such while multiple possible matches are marked as `near` so the user
    can choose the correct match manually.

