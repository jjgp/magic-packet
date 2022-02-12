import csv
import io
import os
import re
import string
import tarfile

import click
from tqdm import tqdm

from magic_packet.cli.utils.lazy_module import tensorflow as tf
from magic_packet.database import DatabaseManager

from . import sql

_EMPTY_SENTENCE_TOKEN = "[empty]"


@click.command()
@click.argument("archive")
@click.argument("database", type=click.Path())
@click.option("-s", "--split", multiple=True, default=["train", "dev", "test"])
def createdb(archive, database, split):
    with DatabaseManager(database) as db_manager, tf.io.gfile.GFile(
        archive, "rb"
    ) as gfile, tarfile.open(mode="r:*", fileobj=gfile) as tar:
        if os.path.exists(database):
            db_manager.execute(sql.drop_all_tables)
        db_manager.create(sql.create_table_clips)
        db_manager.create(sql.create_table_phones)
        db_manager.create(sql.create_table_words)

        n_splits = len(split)
        while n_splits:
            member = tar.next()
            basename = os.path.basename(member.name)
            if "tsv" not in basename:
                continue

            tsv_name = os.path.splitext(basename)[0]
            if tsv_name in split:
                with tar.extractfile(member) as tsv_fobj:
                    _insert_split_into_database(tsv_name, tsv_fobj, db_manager)
                n_splits -= 1

        db_manager.commit()


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
            (clip_id, loc, word.strip(string.punctuation), None, None)
            for loc, word in enumerate(sentence.split())
        ] or [(clip_id, -1, _EMPTY_SENTENCE_TOKEN, None, None)]

        db_manager.execute(sql.insert_into_clips, (clip_id, fname, sentence, split))
        db_manager.executemany(sql.insert_into_words, words)
