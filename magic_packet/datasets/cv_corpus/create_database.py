import argparse
import csv
import io
import os
import tarfile

import tensorflow as tf
from database_manager import DatabaseManager

_SPLIT_FILES = ["train.tsv", "dev.tsv", "test.tsv"]


def main(tar, database, overwrite):
    if not tarfile.is_tarfile(tar):
        return

    if os.path.exists(database) and overwrite:
        # TODO: something to overwrite database
        pass

    with DatabaseManager(database) as db_manager, tf.io.gfile.GFile(
        tar, "rb"
    ) as fobj, tarfile.open(mode="r:*", fileobj=fobj) as tar:
        # TODO: create tsv table in db
        for member in tar:
            if "tsv" in member.name and os.path.basename(member.name) in _SPLIT_FILES:
                _insert_tsv_contents(tar.extractfile(member), db_manager)


def _insert_tsv_contents(tsv_file, db_manager):
    text_wrapper = io.TextIOWrapper(tsv_file, encoding="utf-8")
    tsv = csv.DictReader(text_wrapper, delimiter="\t")

    # TODO: use tqdm here to show progress
    for row in tsv:
        print(row)


def _parser():
    parser = argparse.ArgumentParser(
        description="create the database for the common voice archive contents"
    )
    parser.add_argument("tar", type=str, help="the common voice archive file")
    parser.add_argument("database", type=str, help="the common voice archive file")
    parser.add_argument(
        "--overwrite",
        default=False,
        action=argparse.BooleanOptionalAction,
        help="overwrite existing database if it exists",
    )
    return parser


if __name__ == "__main__":
    # args = _parser().parse_args()
    # main(args.tar, args.database)

    main(
        "./data/cv-corpus-7.0-2021-07-21-en.tar.gz",
        "./data/cv-corpus-7.0-2021-07-21-en.db",
        True,
    )
