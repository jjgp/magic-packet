FROM continuumio/miniconda3

COPY . .

RUN ./apt-get.sh && rm -rf /var/lib/apt/lists/*

RUN conda env create -f amd64.yml \
    && echo "conda activate magic-packet" >> ~/.bashrc
