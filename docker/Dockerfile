FROM nvidia/cuda:11.2.0-cudnn8-runtime-ubuntu20.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    ffmpeg \
    libavcodec-extra \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa -y \
    && apt-get update \
    && apt-get install -y python3.9-dev python3.9-venv \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1

WORKDIR /usr/magic-packet

COPY . .

ENV PATH="/usr/magic-packet/venv/bin:$PATH"

RUN python -m venv venv \
    && pip install -r requirements.txt .

CMD ["magicpkt", "--help"]
