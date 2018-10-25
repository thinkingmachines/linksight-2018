FROM gradle:4.8-jdk8-alpine AS jar
WORKDIR /home/gradle/project
USER root
COPY . .
RUN gradle buildAll

FROM openjdk:8u181-jdk-slim-stretch
RUN apt-get update && \
    apt-get -yy install build-essential git default-jre default-jdk wget && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /setup
COPY deploy/install-zmq.sh .
RUN ./install-zmq.sh && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY data/ data/
COPY --from=jar /home/gradle/project/build/libs/imatch-full-latest.jar .
CMD java -ea -Djava.library.path=/usr/local/lib/ -jar imatch-full-latest.jar -m server -i ipc:///volume/imatch_ipc
