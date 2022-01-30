#!/usr/bin/env bash

pip install --user \
    -r requirements.txt \
    -r requirements-extras.txt \
    -e .

pre-commit install
