# Changelog

## 2018-09-28

- Standardize matchers
- Create staging server
- Upload dataset files to GCS
- Improve reference file
- Switch to Google sign-in tied to an approve emails Google sheet
- Add demo dataset

## 2018-09-21

- Improve user experience
  - CTA for home is now for login/register
  - Move upload to a login-required step
  - Add sidebar on each step with instructions
  - Update match checking step layout
  - Update export step layout
  - Add feedback page
- New matching algorithm

## 2018-09-14

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

## Prototype

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

