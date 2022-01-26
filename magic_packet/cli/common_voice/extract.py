import argparse
import itertools
import os
import tarfile
from collections import namedtuple

from tqdm import tqdm

from magic_packet.cli import argtype
from magic_packet.database import DatabaseManager, sql_join

from .createdb import Clips, Words


def add_to_parser(parser):
    parser.description = "extract clips from the common voice archive"
    parser.add_argument(
        "archive",
        type=argtype.tarfile,
        help="the path to the common voice archive file",
    )
    parser.add_argument(
        "database", type=argtype.path, help="the path to the corpus database"
    )
    parser.add_argument(
        "output_directory", help="the directory to write extracted vocab"
    )
    parser.add_argument(
        "--oov-pct",
        type=int,
        choices=range(0, 101),
        help=(
            "the percentage of OOV clips to extract."
            "if vocab is unspecified, this is ignored."
        ),
        metavar="[0-100]",
    )
    parser.add_argument(
        "--vocab",
        action="append",
        help="the target words to extract",
    )
    parser.set_defaults(func=main)


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


def main(args):
    vocab_clips, oov_clips = query_clips(args.database, args.vocab, args.oov_pct)
    clips = itertools.chain(vocab_clips, oov_clips) if oov_clips else vocab_clips
    extract_clips(clips, args.archive, args.output_directory)


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    add_to_parser(parser)
    args = parser.parse_args()
    args.func(args)
