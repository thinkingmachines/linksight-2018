FROM python:3.6-stretch
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN python3 -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/python manage.py collectstatic --no-input
CMD ["venv/bin/gunicorn", "linksight.wsgi", "-c", "deploy/gunicorn.py"] 
EXPOSE 8000
