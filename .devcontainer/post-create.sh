#!/usr/bin/env bash

apt-get update && apt-get install -y \
    ffmpeg \
    git \
    libavcodec-extra

pip install --user -r requirements.txt

pip install -e .
