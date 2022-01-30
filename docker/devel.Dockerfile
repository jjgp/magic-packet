# sha256 is of the linux/amd64 image
FROM python:3.9.10-slim-buster@sha256:2b97d9dcd0a11b46a884bb7a93cdd529944510b56bbebe19e2111843d6a3ab5d

RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    libavcodec-extra \
    && rm -rf /var/lib/apt/lists/*
