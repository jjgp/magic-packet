FROM continuumio/miniconda3 AS base

ARG HOWL_PACKAGE=https://github.com/castorini/howl/archive/master.zip

RUN apt update && apt install -y \
    build-essential \
    libpulse-dev \
    swig \
    && rm -rf /var/lib/apt/lists/*

COPY environment.yml environment.yml

RUN --mount=type=cache,target=/opt/conda/pkgs \
    conda env create -f environment.yml
