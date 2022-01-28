FROM python:3.9-slim-buster

WORKDIR /usr/magic-packet

COPY . .

RUN python -m venv venv

RUN pip install --no-cache-dir -e .

ENV PATH="/usr/magic-packet/venv/bin:$PATH"

CMD ["magicpkt", "--help"]
