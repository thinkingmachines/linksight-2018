# LinkSight

http://unicefstories.org/2018/04/04/venturefundthinkingmachines/

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

## Contributing

Interested in contributing? Talk to us: hello@thinkingmachin.es
