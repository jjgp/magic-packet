#!/usr/bin/env bash

pip install --user \
    -r requirements.txt \
    -r requirements-extras.txt \
    -e .

# pip install -e .

pre-commit install
