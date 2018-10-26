FROM python:3.6-stretch AS venv
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/testing/
RUN pip install -r testing/requirements.txt
COPY . /usr/src/app/testing
CMD python -m testing.tester
