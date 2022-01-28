FROM nvidia/cuda:11.0-base

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
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

RUN python -m venv venv

ENV PATH="/usr/magic-packet/venv/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install -e .

CMD ["magicpkt", "--help"]
