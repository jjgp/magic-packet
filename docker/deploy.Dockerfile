FROM node:16-bullseye AS base

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1

RUN wget https://bootstrap.pypa.io/get-pip.py \
    && python get-pip.py \
    && rm get-pip.py
