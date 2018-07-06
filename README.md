# LinkSight

http://unicefstories.org/2018/04/04/venturefundthinkingmachines/

## Development

### API

```sh
make
source venv/bin/activate
cp .env{.template,}
# Edit values in .env
python manage.py migrate
python manage.py runserver
```

### App

```sh
cd linksight/app
npm install
npm start
# Catalog
npm run catalog-start
```

## Contributing

Interested in contributing? Talk to us: hello@thinkingmachin.es
