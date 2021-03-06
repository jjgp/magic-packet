import itertools
import os
import tarfile
from collections import namedtuple

import click
from tqdm import tqdm

from magic_packet.database import DatabaseManager, sql_join

from .createdb import Clips, Words


@click.command()
@click.argument("archive", type=click.Path(exists=True))
@click.argument("database", type=click.Path(exists=True))
@click.argument("output_directory")
@click.option("--oov-pct", type=click.FloatRange(1e-5, 100, clamp=True))
@click.option("-v", "--vocab", multiple=True)
def extract(archive, database, output_directory, oov_pct, vocab):
    vocab_clips, oov_clips = query_clips(database, vocab, oov_pct)
    clips = itertools.chain(vocab_clips, oov_clips) if oov_clips else vocab_clips
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


def query_clips(database, vocab=None, oov_pct=None):
    with DatabaseManager(database) as db:
        if vocab:
            vocab_clips = db.join(
                _distinct_clips(),
                where=" or ".join(f"word = '{word}'" for word in vocab),
            )
            oov_clips = (
                db.join(
                    _oov_clips(vocab),
                    where=f"clip_id is null and {_sql_sample_condition(oov_pct / 100)}",
                )
                if oov_pct
                else None
            )
        else:
            vocab_clips, oov_clips = db.select(Clips), None
        return (vocab_clips, oov_clips)


def _abbr_clips_record():
    return namedtuple("AbbrClips", ["fname", "sentence"])


def _distinct_clips():
    return sql_join(Clips, Words, join_type="inner", on="clip_id = id", distinct=True)(
        _abbr_clips_record()
    )


def _oov_clips(vocab):
    words_equal = " or ".join(f"word = '{word}'" for word in vocab)
    return sql_join(
        Clips,
        f"(select clip_id from words where {words_equal})",
        join_type="left",
        on="clip_id = id",
        distinct=True,
    )(_abbr_clips_record())


def _sql_sample_condition(sample_pct):
    return f"abs(cast(random() as real)) / 9223372036854775808 < {sample_pct}"
