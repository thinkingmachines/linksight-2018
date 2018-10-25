FROM python:3.6-stretch AS venv
WORKDIR /usr/src/app
COPY . /usr/src/app/testing
RUN pip install -r testing/requirements.txt
CMD python -m testing.tester
