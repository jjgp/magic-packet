import argparse
import json
import urllib.request

from tqdm import tqdm

_TAR_FORMAT = "cv-corpus-{}-{}.tar.gz"
_URL_FORMAT = (
    "https://commonvoice.mozilla.org/api/v1/bucket/dataset/cv-corpus-{}%2F{}/false"
)


def add_to_parser(parser):
    parser.description = "download the common voice archive file"
    parser.add_argument("directory", type=str, help="the download directory")
    parser.add_argument("--language", type=str, default="en")
    parser.add_argument("--version", type=str, default="7.0-2021-07-21")


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


def main(args):
    download(args.directory, args.language, args.version)


def _tqdm_reporthook(pbar):
    previous_chunk = 0

    def reporthook(chunk, chunk_size, total_size):
        if total_size > -1:
            pbar.total = total_size
        nonlocal previous_chunk
        pbar.update((chunk - previous_chunk) * chunk_size)
        previous_chunk = chunk

    return reporthook


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    add_to_parser(parser)
    main(parser.parse_args())
