FROM ubuntu:20.04

WORKDIR /app

RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
        apt-utils \
        ffmpeg \
        python3-dev \
        build-essential \
        python3 \
        python3-pip && \
    apt-get clean


COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt