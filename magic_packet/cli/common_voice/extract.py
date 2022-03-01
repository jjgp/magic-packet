import itertools
import os
import tarfile

import click
from tqdm import tqdm

from . import sql
from .sqlitedb import SQLiteDB


@click.command()
@click.argument("archive", type=click.Path(exists=True))
@click.argument("database", type=click.Path(exists=True))
@click.argument("output_directory")
@click.option("--between", nargs=2, type=int)
@click.option("--oov-pct", type=click.FloatRange(1e-5, 100, clamp=True))
@click.option("-v", "--vocab", multiple=True)
def extract(archive, database, output_directory, between, oov_pct, vocab):
    if between and (vocab or oov_pct):
        # TODO: implementing a custom option class may be preferable
        # https://stackoverflow.com/a/51235564
        raise click.ClickException(
            "--between and --vocab/--oov-pct are mutually exclusive"
        )

    with SQLiteDB(database) as sqlitedb:
        if between:
            clips = _query_between_clips(sqlitedb, between)
        else:
            vocab_clips, oov_clips = _query_vocab_and_oov_clips(
                sqlitedb, vocab, oov_pct
            )
            clips = (
                itertools.chain(vocab_clips, oov_clips) if oov_clips else vocab_clips
            )

    extract_clips(clips, archive, output_directory)


def extract_clips(clips, archive, output_directory):
    clips_map = {clip.fname: clip.sentence for clip in clips}

    n_clips = len(clips_map)
    if not n_clips:
        raise ValueError("No clips provided")

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    with tqdm(
        total=n_clips, desc="Extracting audio from archive and writing .lab files"
    ) as pbar, tarfile.open(archive, "r|*") as tar:
        while n_clips:
            member = tar.next()
            fname = os.path.basename(member.name)
            if fname in clips_map:
                member.name = fname  # extract only the basename instead of to full path
                output_path = os.path.join(output_directory, fname)
                lab_path = os.path.splitext(output_path)[0] + ".lab"

                tar.extract(member, path=output_directory)
                with open(lab_path, "w") as fobj:
                    fobj.write(clips_map[fname])

                n_clips -= 1
                pbar.update(1)


def _query_between_clips(sqlitedb, between):
    sqlitedb.execute(sql.select_clips_where_id_between, parameters=between)
    return map(sql.Clip._make, sqlitedb.fetchall())


def _query_vocab_and_oov_clips(sqlitedb, vocab, oov_pct):
    n_words = len(vocab)
    sqlitedb.execute(sql.select_clips_where_words_equal(n_words), vocab)
    vocab_clips = map(sql.Clip._make, sqlitedb.fetchall())

    if oov_pct:
        parameters = tuple(vocab) + (oov_pct / 100,)
        sqlitedb.execute(
            sql.select_pct_of_clips_where_words_not_equal(n_words), parameters
        )
        oov_clips = map(sql.Clip._make, sqlitedb.fetchall())
    else:
        oov_clips = None

    return vocab_clips, oov_clips
