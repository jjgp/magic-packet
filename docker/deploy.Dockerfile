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

FROM base AS content-builder

COPY content/Makefile content/Makefile

RUN make -C content -j4 && rm content/*.tar.gz

FROM base AS venv-builder

ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .

RUN python -m venv venv \
    && pip install --no-cache-dir -r requirements.txt

FROM base AS deploy

WORKDIR /usr/deploy

COPY --from=client-builder build client/build

COPY --from=content-builder content/multilingual_embedding content/multilingual_embedding

COPY --from=content-builder content/multilingual_kws content/multilingual_kws

COPY --from=content-builder content/speech_commands/_background_noise_ content/_background_noise_

COPY --from=content-builder content/unknown_files content/unknown_files

COPY --from=venv-builder venv venv

ENV PYTHONPATH=content/multilingual_kws:/usr/deploy/venv

ENV PATH="/usr/deploy/venv/bin:$PATH"

COPY api api

COPY app.py .

CMD ["uvicorn", "app:app"]
