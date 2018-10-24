# TODO: change below to smaller linux image -- alpine?
FROM gradle:4.8-jdk8-alpine AS gradle
WORKDIR /home/gradle/project
USER root
COPY . .
RUN gradle dependencies
#COPY . .
RUN gradle buildAll
#RUN ./gradlew buildAll


FROM openjdk:8u181-jdk-slim-stretch
RUN apt-get update && \
    apt-get -yy install build-essential git default-jre default-jdk wget && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /setup
COPY deploy/install-zmq.sh .
RUN ./install-zmq.sh && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY build/libs/imatch-full-latest.jar .