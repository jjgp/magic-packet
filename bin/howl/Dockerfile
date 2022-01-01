FROM python:3.7-slim-buster

ARG HOWL_ZIP_URL=https://github.com/castorini/howl/archive/5b9f25869385347ccdc904beccba0f1a9fd495c9.zip
ARG HOWL_MODELS_ZIP_URL=https://github.com/castorini/howl-models/archive/052041e0f51fc00dc050ecc4f5df8ea57bf2e047.zip

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libpulse-dev \
    portaudio19-dev \
    python-all-dev \
    swig \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN curl -L $HOWL_ZIP_URL -o howl.zip \
    && unzip howl.zip \
    && mv howl-* howl \
    && curl -L $HOWL_MODELS_ZIP_URL -o howl-models.zip \
    && unzip howl-models.zip \
    && mv howl-models-*/* howl/howl-models

WORKDIR /howl

RUN --mount=type=cache,mode=0777,target=/.cache/pip

ENV PATH="/howl/env/bin:$PATH"

RUN python3 -m venv env \
    && pip install --upgrade pip \
    && pip install -r requirements.txt -r requirements_training.txt

FROM python:3.7-slim-buster

ENV PATH="/howl/env/bin:$PATH"

WORKDIR /howl

COPY --from=0 /howl /howl

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1-dev \
    && rm -rf /var/lib/apt/lists/*
