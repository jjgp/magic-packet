import csv
import io
import os
import re
import string
import tarfile

import click
from tqdm import tqdm

from magic_packet.cli.utils.lazy_module import tensorflow as tf

from . import sql
from .sqlitedb import SQLiteDB

_EMPTY_SENTENCE_TOKEN = "[empty]"


@click.command()
@click.argument("archive")
@click.argument("database", type=click.Path())
@click.option("-s", "--split", multiple=True, default=["train", "dev", "test"])
def createdb(archive, database, split):
    with SQLiteDB(database) as sqlitedb, tf.io.gfile.GFile(
        archive, "rb"
    ) as gfile, tarfile.open(mode="r:*", fileobj=gfile) as tar:
        for statement in sql.DROP_TABLES + sql.CREATE_TABLES:
            sqlitedb.execute(statement)

        n_splits = len(split)
        while n_splits:
            member = tar.next()
            basename = os.path.basename(member.name)
            if "tsv" not in basename:
                continue

            tsv_name = os.path.splitext(basename)[0]
            if tsv_name in split:
                with tar.extractfile(member) as tsv_fobj:
                    _insert_split_into_database(tsv_name, tsv_fobj, sqlitedb)
                n_splits -= 1


def _insert_split_into_database(split, tsv_fobj, sqlitedb):
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
            sql.Utterance(clip_id, loc, word.strip(string.punctuation))
            for loc, word in enumerate(sentence.split())
        ] or [sql.Utterance(clip_id, -1, _EMPTY_SENTENCE_TOKEN)]

        sqlitedb.execute(
            sql.INSERT_INTO_CLIPS, sql.Clip(clip_id, fname, sentence, split)
        )
        sqlitedb.executemany(sql.INSERT_INTO_WORDS, words)
