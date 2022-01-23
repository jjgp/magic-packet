# flake8: noqa

import argparse
import io
import os
import tarfile
import warnings

import librosa
import soundfile
from montreal_forced_aligner.config import get_temporary_directory
from montreal_forced_aligner.models import AcousticModel
from pydub import AudioSegment
from tqdm import tqdm

from magic_packet.datasets.cv_corpus.database.database_manager import DatabaseManager
from magic_packet.datasets.cv_corpus.database.records import WordsOnClips
from magic_packet.utils import argtype

_SAMPLE_RATE = 16000
_MONO = False


def main(
    vocab,
    archive,
    database,
    dictionary,
    acoustic_model,
    output_directory,
    working_directory,
):
    # TODO: need to query the alignments to see if they already exist
    words_on_clips = _query_words_on_clips(vocab, database)

    # TODO: probably need to a mapping of words, clips, and alignments

    # TODO: need to make extract folder

    # TODO: need to use multiprocessing to extract the vocab

    # Extract clips as wavs with corresponding .lab file to working directory
    _extract_words_on_clips(words_on_clips, archive, working_directory)

    if acoustic_model in AcousticModel.get_available_models():
        pretrained_path = AcousticModel.get_pretrained_path(acoustic_model)
    else:
        pass
    mfa_directory = get_temporary_directory()

    acoustic_model = AcousticModel(pretrained_path)
    pass


def _convert_mp3_to_wav(fobj, output_path):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        audio = librosa.core.load(fobj, sr=_SAMPLE_RATE, mono=_MONO)[0]
    soundfile.write(output_path, audio, _SAMPLE_RATE)


def _extract_words_on_clips(words_on_clips, archive, working_directory):
    clips_directory = f"{working_directory}/clips"
    clips = {fname: sentence for _, fname, _, _, sentence, _ in words_on_clips}
    with tarfile.open(archive, "r:*") as tar:
        for member in tar:
            fname = os.path.basename(member.name)
            if fname in clips:
                with tar.extractfile(member) as fobj:
                    data, sr = soundfile.read(io.BytesIO(fobj.read()))
                    pass
                # if not os.path.exists(f"{clips_directory}/{fname}"):
                #     member.name = fname  # extract only the basename instead of to full path
                #     tfile.extract(member, path=clips_directory)


def _query_words_on_clips(vocab, database):
    with DatabaseManager(database) as db:
        return db.join(
            WordsOnClips, where=" or ".join(f"word = '{word}'" for word in vocab)
        )


def _parser():
    # TODO: need a num jobs argument and use mp logic from howl to derive cpu count
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
        args.archive,
        args.database,
        args.dictionary,
        args.acoustic_model,
        args.output_directory,
        args.working_directory,
    )
