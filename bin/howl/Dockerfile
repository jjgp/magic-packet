FROM python:3.6-slim-buster

ARG HOWL_ZIP_URL=https://github.com/castorini/howl/archive/5b9f25869385347ccdc904beccba0f1a9fd495c9.zip

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
    && mv howl-* howl

WORKDIR /howl

RUN --mount=type=cache,mode=0777,target=/.cache/pip

ENV PATH="/howl/env/bin:$PATH"

RUN python3 -m venv env \
    && pip install --upgrade pip \
    && pip install -r requirements.txt -r requirements_training.txt

FROM python:3.6-slim-buster

RUN apt-get update && apt-get install -y \
    libsndfile1-dev \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/howl/env/bin:$PATH"

WORKDIR /howl

COPY --from=0 /howl /howl
