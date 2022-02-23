FROM ubuntu:18.04

ENV LANG C.UTF-8

RUN apt-get update \
    && apt-get install -y build-essential python3-dev python3-pip python3-numpy-dev python3-six \
       libfftw3-3 libyaml-0-2 libtag1v5 libsamplerate0 python3-yaml \
       libavcodec57 libavformat57 libavutil55 libavresample3 wget pkg-config libeigen3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip setuptools \
    && pip3 install --no-cache-dir tensorflow==1.15.0

RUN apt-get update \
    && apt-get install -y build-essential python3-dev git \
       libfftw3-dev libavcodec-dev libavformat-dev libavresample-dev \
       libsamplerate0-dev libtag1-dev libyaml-dev \
    && mkdir /essentia && mkdir -p /usr/local/lib/pkgconfig \
    && cd /essentia && git clone https://github.com/MTG/essentia.git \
    && cd /essentia/essentia && src/3rdparty/tensorflow/setup_from_python.sh \
    \
    # patch as discussed in https://github.com/MTG/essentia-docker/pull/7#discussion_r380782792
    && echo "Requires: python3" >> /usr/local/lib/pkgconfig/tensorflow.pc \
    \
    && python3 waf configure --build-static --with-python --with-examples --with-vamp --with-tensorflow \
    && python3 waf && python3 waf install && ldconfig \
    && apt-get remove -y build-essential libyaml-dev libfftw3-dev libavcodec-dev \
       libavformat-dev libavutil-dev libavresample-dev libsamplerate0-dev \
      libtag1-dev python3-numpy-dev \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
    && cd / && rm -rf /essentia/essentia

RUN apt-get update -y \
    && apt-get install libasound2-dev alsa-base alsa-utils pulseaudio -y \
    && pip install pyalsaaudio


# RUN apt-get install pulseaudio -y

ENV PYTHONPATH /usr/local/lib/python3/dist-packages

WORKDIR /essentia

RUN pip install scipy numpy

#COPY rock.mp3 rock.mp3
#COPY rock.wav rock.wav
#COPY extractor_metadata.py extractor_metadata.py
COPY predict_genre.py predict_genre.py
COPY msd-musicnn-1.json msd-musicnn-1.json
COPY msd-musicnn-1.pb msd-musicnn-1.pb

RUN export PULSE_SERVER=tcp:127.0.0.1