import argparse
import csv
import io
import os
import re
import string
import tarfile

import tensorflow as tf
from database_manager import ClipsTable, DatabaseManager, WordsTable
from tqdm import tqdm

_SPLITS = ["train", "dev", "test"]


def main(tar, database, overwrite):
    if not tarfile.is_tarfile(tar):
        # TODO: logger early exit
        return

    database_exists = os.path.exists(database)
    if database_exists and not overwrite:
        # TODO: logger early exit
        return

    with DatabaseManager(database) as db_manager, tf.io.gfile.GFile(
        tar, "rb"
    ) as gfile, tarfile.open(mode="r:*", fileobj=gfile) as tar:
        if database_exists:
            db_manager.drop_tables()
        db_manager.create_tables()

        splits_left = len(_SPLITS)
        while splits_left:
            member = tar.next()
            basename = os.path.basename(member.name)
            if "tsv" not in basename:
                continue

            split = os.path.splitext(basename)[0]
            if split in _SPLITS:
                tsv_fobj = tar.extractfile(member)
                _insert_split_into_database(split, tsv_fobj, db_manager)
                splits_left -= 1


def _iter_words(sentence):
    for loc, word in enumerate(sentence.split()):
        without_punctuation = word.strip(string.punctuation)
        yield loc, without_punctuation


def _insert_split_into_database(split, tsv_fobj, db_manager):
    io_wrapper = io.TextIOWrapper(tsv_fobj, encoding="utf-8")
    total = sum(1 for _ in io_wrapper) - 1  # -1 for header
    io_wrapper.seek(0)
    reader = csv.DictReader(io_wrapper, delimiter="\t")

    p = re.compile(r"^[a-zA-Z_]+(\d+)\.mp3$")
    for row in tqdm(reader, desc=f"inserting {split} ", total=total):
        path, sentence = row["path"], row["sentence"].lower()
        match = p.match(path)
        if not match:
            continue
        clip_id = match.group(1)
        db_manager.insert(ClipsTable.name, (clip_id, split, path))
        words = ((clip_id, loc, word) for loc, word in _iter_words(sentence))
        db_manager.insert_many(WordsTable.name, words)


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
        "./data/cv-corpus-7.0-2021-07-21/en/index.db",
        True,
    )
