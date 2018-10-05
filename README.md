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
    | DATABASE_URL | See [DJ-Database-URL](https://github.com/kennethreitz/dj-database-url) |
    | SECRET_KEY | String used to provide cryptographic signing of sessions, etc. |
    | EMAIL_PORT | Port to use when sending email |
    | EMAIL_HOST_USER | User for sending email |
    | EMAIL_HOST_PASSWORD | Password for above |
    | SOCIAL_AUTH_GOOGLE_OAUTH2_KEY | Key for Google OAuth2 |
    | SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET | Secret for Google OAuth2 |
    | GOOGLE_APPLICATION_CREDENTIALS | Path to the Google Cloud Service Account key file used to retrieve the list of approved emails |
    | APPROVED_EMAILS_SHEET_ID | Google Sheets ID of th list of approved emails |
    | APPROVED_EMAILS_SHEET_RANGE | The sheet range for approved emails |
    | APPROVED_EMAILS_ROW_KEY | The row key for approved emails |

    If you are a member of the official LinkSight development team, you can ask
    for access to the template with secrets filled in.

1. Install postgresql and run the following in `psql`:

    ```
    CREATE DATABASE linksight;
    ```

    Make sure that you can connect using the `DATABASE_URL` you used in `.env`.

1. Run the server

    ```sh
    source venv/bin/activate
    python manage.py migrate
    python manage.py runserver
    ```

1. Go to [http://localhost:3000/](http://localhost:3000/)

### Components Catalog

```sh
npm run catalog-start
```

### Testing

```sh
gunzip -k data/clean-psgc.csv.gz
python manage.py test
```

You can run specific subsets of tests [like so](https://docs.djangoproject.com/en/2.1/topics/testing/overview/#running-tests).

### Deployment

#### Staging

```sh
cd deploy
make
```

#### Production

Instructions to follow.
