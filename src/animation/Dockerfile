FROM alpine:latest

ENV LANG C.UTF-8

RUN apt-get update \
    && apt-get -y upgrade

RUN apt-get install python3-dev python3-pip

RUN pip install numpy colormath pandas

RUN pip install redis

RUN pip install adafruit-circuitpython-neopixel

WORKDIR /animation

COPY . .
