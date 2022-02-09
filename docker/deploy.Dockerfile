FROM node:16-bullseye AS base

RUN apt-get update && apt-get install -y \
    locales \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

ENV LANG en_US.utf8

RUN apt-get install -y python3-venv \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1

FROM base AS client-builder

COPY client .

RUN npm i && PUBLIC_URL="http://localhost:5000/" npm run build

FROM base AS deploy

WORKDIR /usr/deploy

COPY --from=client-builder build client/build

COPY api api

COPY app.py requirements.txt ./

ENV PATH="/usr/deploy/venv/bin:$PATH"

RUN python -m venv venv \
    && pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
