# LinkSight

This web app takes a list of barangay, municipality, city, and province names and looks up their closest matches in the [Philippine Standard Geographic Code (PSGC)](http://nap.psa.gov.ph/activestats/psgc/default.asp). It's useful if you're trying to standardize location names for merging location datasets from diverse sources.

## How it works

1. Upload a single CSV file that contains separate barangay, province, and city or municipality columns.
2. Identify the columns that correspond to the correct administrative levels in the PSG code.
3. For places with exact matches in the PSGC, LinkSight returns the precise PSG code. For places with more than one possible matching PSG code, use the app's graphical user interface to select the correct match.
4. Export the results as a CSV.

## Feedback

This app is in active development! Your feedback will help us improve it. If you
have any suggestions for features, enhancements, or find any bugs, or just want
to contribute, please send us an email at
[linksight@thinkingmachin.es](mailto:linksight@thinkingmachin.es).

## Development

### React App

1. Install dependencies

    ```sh
    cd app
    npm install
    ```

1. Run server

    ```sh
    npm start
    ```

### Django API

1. Install dependencies

    ```sh
    make install
    ```

1. Set configuration values

    ```
    cp .env{.template,}
    ```

    | Config name | Description |
    | - | - |
    | DEBUG | Toggles running the server in debug mode |
    | DATABASE_URL | https://github.com/kennethreitz/dj-database-url |
    | SECRET_KEY | String used to provide cryptographic signing of sessions, etc. |
    | PSGC_DATASET_ID | UUID of PSGC reference dataset |
    | POPULATION_DATASET_ID | UUID of the population dataset |

    Instructions will follow on how to set `PSGC_DATASET_ID` and `POPULATION_DATASET_ID`.

1. Install postgresql and run the following in `psql`:

    ```
    CREATE DATABASE unicef;
    ```

    Make sure that you can connect using the `DATABASE_URL` you used in `.env`.

1. Run server

    ```sh
    source venv/bin/activate
    python manage.py migrate
    python manage.py runserver
    ```

1. Upload the dataset files

    - Download the files from [this bucket](https://console.cloud.google.com/storage/browser/linksight?project=linksight-208514&organizationId=301224238109).
    - Go to `http://localhost:3000/` on your browser and upload them one at a time.
        - After uploading `clean-psgc.csv`, use the ID in the post-upload URL to fill in `PSGC_DATASET_ID` in `.env`
        - After uploading `population.csv`, use the ID in the post-upload URL to fill in `POPULATION_DATASET_ID` in `.env`
    - After updating `.env`, restart your server.

    ```sh
    python manage.py runserver
    ```

### Components Catalog

```sh
npm run catalog-start
```
