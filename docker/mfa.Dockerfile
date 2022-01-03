FROM continuumio/miniconda3

RUN --mount=type=cache,target=/opt/conda/pkgs \
    conda create -n aligner -c conda-forge montreal-forced-aligner

RUN conda run --no-capture-output -n aligner \
    mfa model download acoustic english

ENTRYPOINT [ "conda", "run", "--no-capture-output", "-n", "aligner" ]
