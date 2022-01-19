import argparse
import csv
import io
import os
import re
import string
import tarfile

import tensorflow as tf
from database_manager import DatabaseManager
from tqdm import tqdm

_SPLITS = ["train", "dev", "test"]


def main(tar, database, overwrite):
    if not tarfile.is_tarfile(tar):
        return

    if os.path.exists(database) and not overwrite:
        pass

    # TODO: create tsv table in db
    with DatabaseManager(database) as db_manager, tf.io.gfile.GFile(
        tar, "rb"
    ) as gfile, tarfile.open(mode="r:*", fileobj=gfile) as tar:
        # TODO: don't use _cur directly
        db_manager._cur.execute(
            "create table clips (id integer primary key, split varchar, name varchar)"
        )
        db_manager._cur.execute(
            "create table words (clip_id integer, loc integer, word varchar)"
        )

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

    # TODO: use tqdm here to show progress
    p = re.compile(r"^[a-zA-Z_]+(\d+)\.mp3$")
    for row in tqdm(reader, desc=f"inserting {split} ", total=total):
        path, sentence = row["path"], row["sentence"].lower()
        match = p.match(path)
        if not match:
            continue
        clip_id = match.group(1)
        db_manager._cur.execute(
            "insert into clips values (?, ?, ?)", (clip_id, split, path)
        )
        words = ((clip_id, loc, word) for loc, word in _iter_words(sentence))
        db_manager._cur.executemany("insert into words values (?, ?, ?)", words)
    db_manager._conn.commit()


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
