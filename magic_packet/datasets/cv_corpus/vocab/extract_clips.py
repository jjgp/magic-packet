import argparse
import os
import tarfile

from tqdm import tqdm

from magic_packet.datasets.cv_corpus.database.database_manager import DatabaseManager
from magic_packet.datasets.cv_corpus.database.records import Clips, DistinctClips
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
                with open(lab_path, "a") as fobj:
                    fobj.write(clips_map[fname])

                n_clips -= 1
                pbar.update(1)


def main(vocab, archive, database, output_directory):
    clips = _query_clips(database, vocab)
    extract_clips(clips, archive, output_directory)


def _query_clips(database, vocab):
    with DatabaseManager(database) as db:
        if vocab:
            return db.join(
                DistinctClips, where=" or ".join(f"word = '{word}'" for word in vocab)
            )
        else:
            return db.select(Clips)


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
        "--vocab",
        nargs="+",
        type=str,
        help="the working directory to write intermediate artifacts",
    )
    return parser


if __name__ == "__main__":
    args = _parser().parse_args()
    main(args.vocab, args.archive, args.database, args.output_directory)
