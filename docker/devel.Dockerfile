FROM python:3.9.10-slim-buster

RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    libavcodec-extra \
    && rm -rf /var/lib/apt/lists/*
