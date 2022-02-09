FROM node:16-bullseye AS base

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1
