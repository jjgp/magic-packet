import argparse
import csv
import io
import logging
import os
import re
import string
import tarfile

import tensorflow as tf
from database.database_manager import DatabaseManager
from database.records import Clips, Words
from tqdm import tqdm

logger = logging.getLogger(__name__)


def main(tar, database, overwrite, splits):
    if not tarfile.is_tarfile(tar):
        logger.error(f"{tar} is not a tar file")
        return

    database_exists = os.path.exists(database)
    if database_exists and not overwrite:
        logger.error(f"Database {database} exists and overwrite is {overwrite}")
        return

    with DatabaseManager(database) as db_manager, tf.io.gfile.GFile(
        tar, "rb"
    ) as gfile, tarfile.open(mode="r:*", fileobj=gfile) as tar:
        if database_exists:
            db_manager.drop(Clips, Words)
        db_manager.create(Clips, Words)

        n_splits = len(splits)
        while n_splits:
            member = tar.next()
            basename = os.path.basename(member.name)
            if "tsv" not in basename:
                continue

            split = os.path.splitext(basename)[0]
            if split in splits:
                tsv_fobj = tar.extractfile(member)
                _insert_split_into_database(split, tsv_fobj, db_manager)
                n_splits -= 1

        db_manager.commit()


def _insert_split_into_database(split, tsv_fobj, db_manager):
    io_wrapper = io.TextIOWrapper(tsv_fobj, encoding="utf-8")
    total = sum(1 for _ in io_wrapper) - 1  # -1 for TSV header
    io_wrapper.seek(0)
    reader = csv.DictReader(io_wrapper, delimiter="\t")

    clip_id_pattern = re.compile(r"^[a-zA-Z_]+(\d+)\.mp3$")
    for row in tqdm(reader, desc=f"Inserting {split} into database", total=total):
        fname, sentence = row["path"], row["sentence"].lower()
        match = clip_id_pattern.match(fname)
        if not match:
            continue

        clip_id = match.group(1)
        words = [
            Words(clip_id, loc, word.strip(string.punctuation))
            for loc, word in enumerate(sentence.split())
        ]
        if not words:
            continue

        db_manager.insert(Clips(clip_id, fname, split))
        db_manager.insertmany(words)


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
    parser.add_argument(
        "--splits",
        nargs="+",
        default=["train", "dev", "test"],
        help="the splits to include in the database",
    )
    return parser


if __name__ == "__main__":
    args = _parser().parse_args()
    main(args.tar, args.database, args.overwrite, args.splits)
