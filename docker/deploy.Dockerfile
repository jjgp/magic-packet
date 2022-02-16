FROM node:16-bullseye AS base

RUN apt-get update && apt-get install -y \
    libsndfile1 \
    locales \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

ENV LANG en_US.utf8

RUN apt-get install -y python3-venv \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1

FROM base AS client-builder

ARG PUBLIC_URL=/client

COPY client .

RUN npm i && PUBLIC_URL=$PUBLIC_URL npm run build

FROM base AS deploy

ENV PATH="/usr/deploy/venv/bin:$PATH"

WORKDIR /usr/deploy

COPY --from=client-builder build client/build

COPY api api

COPY app.py requirements.txt Makefile ./

RUN make content

RUN python -m venv venv \
    && pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app:app"]
