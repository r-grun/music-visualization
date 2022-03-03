FROM alpine:latest

ENV LANG C.UTF-8

RUN apt-get update \
    && apt-get -y upgrade

RUN apt-get install python3-dev python3-pip

RUN pip install numpy colormath pandas

WORKDIR /animation

COPY . .
