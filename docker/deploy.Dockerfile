FROM tensorflow/tensorflow:2.7.0 AS base

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get update && apt-get install -y \
    libsndfile1 \
    nodejs

FROM base AS client-builder

ARG PUBLIC_URL=/client

COPY client .

RUN npm i && PUBLIC_URL=$PUBLIC_URL npm run build

FROM base AS content-builder

COPY content/Makefile content/Makefile

RUN make -C content -j4 && rm content/*.tar.gz

FROM base AS deploy

WORKDIR /usr/deploy

ENV PYTHONPATH=content/multilingual_kws

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --from=client-builder build client/build

COPY --from=content-builder content/multilingual_embedding content/multilingual_embedding

COPY --from=content-builder content/multilingual_kws content/multilingual_kws

COPY --from=content-builder content/speech_commands/_background_noise_ content/speech_commands/_background_noise_

COPY --from=content-builder content/unknown_files content/unknown_files

COPY api api

COPY app.py .

CMD ["uvicorn", "app:app"]
