FROM python:3.6-stretch
COPY . /usr/src/app
WORKDIR /usr/src/app
CMD ["venv/bin/gunicorn", "linksight.wsgi", "-c", "deploy/gunicorn.py"]
EXPOSE 8000
