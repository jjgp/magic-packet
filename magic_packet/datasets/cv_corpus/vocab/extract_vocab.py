# flake8: noqa

import argparse
import tarfile

from montreal_forced_aligner.config import get_temporary_directory
from montreal_forced_aligner.models import AcousticModel

from magic_packet.datasets.cv_corpus.database.database_manager import DatabaseManager
from magic_packet.datasets.cv_corpus.database.records import WordsOnClips
from magic_packet.utils import argtype


def query_words_on_clips(vocab, database):
    with DatabaseManager(database) as db:
        return db.join(
            WordsOnClips, where=" or ".join(f"word = '{word}'" for word in vocab)
        )


def main(
    vocab,
    tar,
    database,
    dictionary,
    acoustic_model,
    output_directory,
    working_directory,
):
    # TODO: need to query the alignments to see if they already exist
    words_on_clips = query_words_on_clips(vocab, database)

    # Extract clips to working directory

    if acoustic_model in AcousticModel.get_available_models():
        pretrained_path = AcousticModel.get_pretrained_path(acoustic_model)
    else:
        pass
    mfa_directory = get_temporary_directory()

    acoustic_model = AcousticModel(pretrained_path)
    pass


def _parser():
    # TODO: need a num jobs argument and use mp logic from howl to derive cpu count
    parser = argparse.ArgumentParser(
        description="extract the vocab audio from the common voice archive"
    )
    parser.add_argument(
        "tar", type=argtype.tarfile, help="the path to the common voice archive file"
    )
    parser.add_argument(
        "database", type=argtype.path, help="the path to the corpus database"
    )
    parser.add_argument(
        "dictionary", type=str, help="the path to the pronunciation dictionary"
    )
    parser.add_argument("acoustic_model", type=str, help="the saved model name")
    parser.add_argument(
        "output_directory", type=str, help="the directory to write extracted vocab"
    )
    parser.add_argument(
        "working_directory",
        type=str,
        help="the working directory to write intermediate artifacts",
    )
    parser.add_argument(
        "--vocab",
        nargs="+",
        default=["hey", "fire", "fox"],
        type=str,
        help="the working directory to write intermediate artifacts",
    )
    return parser


if __name__ == "__main__":
    args = _parser().parse_args()
    main(
        args.vocab,
        args.tar,
        args.database,
        args.dictionary,
        args.acoustic_model,
        args.output_directory,
        args.working_directory,
    )
