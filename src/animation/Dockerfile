FROM ubuntu:21.04

ENV LANG C.UTF-8

RUN apt-get update \
    && apt-get -y upgrade \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y python3-numpy python3-pip

RUN pip install numpy colormath pandas

RUN pip install redis

RUN pip install adafruit-circuitpython-neopixel

WORKDIR /animation

COPY . .
