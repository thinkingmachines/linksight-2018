# LinkSight

http://unicefstories.org/2018/04/04/venturefundthinkingmachines/

## Development

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

    _You can run the server and use the frontend to upload the dataset files:_

    https://console.cloud.google.com/storage/browser/linksight?project=linksight-208514&organizationId=301224238109

1. Run server

    ```sh
    source venv/bin/activate
    python manage.py migrate
    python manage.py runserver
    ```

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

### Components Catalog

```sh
npm run catalog-start
```

## Contributing

Interested in contributing? Talk to us: hello@thinkingmachin.es
