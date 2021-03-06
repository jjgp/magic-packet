import json
import urllib.request

import click
from tqdm import tqdm

_TAR_FORMAT = "cv-corpus-{}-{}.tar.gz"
_URL_FORMAT = (
    "https://commonvoice.mozilla.org/api/v1/bucket/dataset/cv-corpus-{}%2F{}/false"
)


@click.command()
@click.argument("directory")
@click.option("-l", "--language", default="en")
@click.option("-v", "--version", default="7.0-2021-07-21")
def download(directory, language, version):
    tar = _TAR_FORMAT.format(version, language)
    url = _URL_FORMAT.format(version, tar)
    with urllib.request.urlopen(url) as response:
        download_url = json.loads(response.read().decode())["url"]

    with tqdm(
        desc=tar, miniters=1, unit="B", unit_scale=True, unit_divisor=1024
    ) as pbar:
        urllib.request.urlretrieve(
            download_url, f"{directory}/{tar}", reporthook=_tqdm_reporthook(pbar)
        )


def _tqdm_reporthook(pbar):
    previous_chunk = 0

    def reporthook(chunk, chunk_size, total_size):
        if total_size > -1:
            pbar.total = total_size
        nonlocal previous_chunk
        pbar.update((chunk - previous_chunk) * chunk_size)
        previous_chunk = chunk

    return reporthook
