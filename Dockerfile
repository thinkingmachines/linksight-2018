FROM openjdk:8u181-jdk-slim-stretch
RUN apt-get update && \
    apt-get -yy install build-essential git default-jre default-jdk && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /setup
COPY deploy/ .
RUN ./install-zmq.sh
WORKDIR /app
COPY build/libs/imatch-full-latest.jar .
