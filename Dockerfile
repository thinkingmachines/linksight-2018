FROM openjdk:8u181-jdk-slim-stretch
RUN apt-get update && \
    apt-get -yy install build-essential git default-jre default-jdk wget && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /setup
COPY deploy/ .
RUN ./install-zmq.sh && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY build/libs/imatch-full-latest.jar .