import argparse
import itertools
import os
import tarfile
from collections import namedtuple

from tqdm import tqdm

from magic_packet.datasets.cv_corpus.database.database_manager import DatabaseManager
from magic_packet.datasets.cv_corpus.database.records import Clips, Words, sql_join
from magic_packet.utils import argtype


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


def main(vocab, oov_pct, archive, database, output_directory):
    vocab_clips, oov_clips = query_clips(database, vocab, oov_pct)
    clips = itertools.chain(vocab_clips, oov_clips) if oov_clips else vocab_clips
    extract_clips(clips, archive, output_directory)


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


def _abbr_clips_record(name):
    return namedtuple(name, ["fname", "sentence"])


def _distinct_clips():
    record = _abbr_clips_record("DistinctClips")
    return sql_join(Clips, Words, join_type="inner", on="clip_id = id", distinct=True)(
        record
    )


def _oov_clips(vocab):
    record = _abbr_clips_record("OOVClips")
    words_equal = " or ".join(f"word = '{word}'" for word in vocab)
    return sql_join(
        Clips,
        f"(select clip_id from words where {words_equal})",
        join_type="left",
        on="clip_id = id",
        distinct=True,
    )(record)


def _parser():
    parser = argparse.ArgumentParser(
        description="extract the vocab audio from the common voice archive"
    )
    parser.add_argument(
        "archive",
        type=argtype.tarfile,
        help="the path to the common voice archive file",
    )
    parser.add_argument(
        "database", type=argtype.path, help="the path to the corpus database"
    )
    parser.add_argument(
        "output_directory", type=str, help="the directory to write extracted vocab"
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
        nargs="+",
        type=str,
        help="the working directory to write intermediate artifacts",
    )
    return parser


def _sql_sample_condition(sample_pct):
    return f"abs(cast(random() as real)) / 9223372036854775808 < {sample_pct}"


if __name__ == "__main__":
    args = _parser().parse_args()
    main(args.vocab, args.oov_pct, args.archive, args.database, args.output_directory)
