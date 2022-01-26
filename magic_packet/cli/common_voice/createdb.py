import argparse
import csv
import io
import logging
import os
import re
import string
import tarfile
from typing import NamedTuple

import tensorflow as tf
from tqdm import tqdm

from magic_packet.cli import argtype
from magic_packet.database import DatabaseManager, sql_table

_EMPTY_SENTENCE_TOKEN = "[empty]"

logger = logging.getLogger(__name__)


@sql_table(primary_keys=["id"])
class Clips(NamedTuple):
    id: int
    fname: str
    sentence: str
    split: str


@sql_table(primary_keys=["clip_id", "loc"])
class Words(NamedTuple):
    clip_id: int
    loc: int
    word: str


def add_to_parser(parser):
    parser.description = "create the database for the common voice archive contents"
    parser.add_argument(
        "archive",
        type=argtype.tarfile,
        help="the path to the common voice archive file",
    )
    parser.add_argument("database", help="the path to the corpus database")
    parser.add_argument(
        "--overwrite",
        default=False,
        action=argparse.BooleanOptionalAction,
        help="overwrite existing database if it exists",
    )
    parser.add_argument(
        "-s",
        "--splits",
        nargs="+",
        default=["train", "dev", "test"],
        help="the splits to include in the database",
    )
    parser.set_defaults(func=main)


def createdb(archive, database, overwrite, splits):
    database_exists = os.path.exists(database)
    if database_exists and not overwrite:
        logger.error(f"Database {database} exists and overwrite is {overwrite}")
        return

    with DatabaseManager(database) as db_manager, tf.io.gfile.GFile(
        archive, "rb"
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
                with tar.extractfile(member) as tsv_fobj:
                    _insert_split_into_database(split, tsv_fobj, db_manager)
                n_splits -= 1

        db_manager.commit()


def main(args):
    createdb(args.archive, args.database, args.overwrite, args.splits)


def _insert_split_into_database(split, tsv_fobj, db_manager):
    io_wrapper = io.TextIOWrapper(tsv_fobj, encoding="utf-8")
    total = sum(1 for _ in io_wrapper) - 1  # - 1 for TSV header
    io_wrapper.seek(0)
    reader = csv.DictReader(io_wrapper, delimiter="\t")

    clip_id_pattern = re.compile(r"^[a-zA-Z_]+(\d+)\.mp3$")
    for row in tqdm(reader, desc=f"Inserting {split} split into database", total=total):
        fname, sentence = row["path"], row["sentence"].lower()
        match = clip_id_pattern.match(fname)
        if not match:
            continue

        clip_id = match.group(1)
        words = [
            Words(clip_id, loc, word.strip(string.punctuation))
            for loc, word in enumerate(sentence.split())
        ] or [Words(clip_id, -1, _EMPTY_SENTENCE_TOKEN)]

        db_manager.insert(Clips(clip_id, fname, sentence, split))
        db_manager.insertmany(words)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    add_to_parser(parser)
    args = parser.parse_args()
    args.func(args)
