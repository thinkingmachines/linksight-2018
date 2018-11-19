FROM gradle:4.8-jdk8-alpine AS jar
WORKDIR /home/gradle/project
USER root
COPY . .
RUN gradle buildAll

FROM openjdk:8u181-jdk-slim-stretch
COPY --from=jar /home/gradle/project/build/libs/imatch-full-latest.jar .
CMD java -ea -Djava.library.path=/usr/local/lib/ -jar imatch-full-latest.jar -m server -i ipc:///volume/imatch_ipc
