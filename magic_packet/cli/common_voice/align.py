import atexit
from argparse import Namespace

import click
from montreal_forced_aligner import command_line
from montreal_forced_aligner.alignment import PretrainedAligner
from montreal_forced_aligner.config import get_temporary_directory
from montreal_forced_aligner.utils import check_third_party
from tqdm import tqdm

from .sqlitedb import SQLiteDB


@click.command()
@click.argument("database", type=click.Path(exists=True))
@click.argument("corpus_directory")
@click.argument("dictionary_path")
@click.argument("acoustic_model_path")
@click.argument("output_directory")
@click.option("-t", "--temporary_directory", default=get_temporary_directory())
@click.option("--config_path", default="0")
@click.option("-s", "--speaker_characters", default="0")
@click.option("-a", "--audio_directory", default="")
@click.option("-j", "--num_jobs", type=int, default=1)
@click.option("--debug", is_flag=True)
@click.option("--verbose", is_flag=True)
@click.option("--clean", is_flag=True)
@click.option("--overwrite", is_flag=True)
def align(**kwargs):
    """
    run pretrained aligner from montreal-forced-aligner

    more info on args, see montreal_forced_aligner/command_line/mfa.py
    """

    _mfa_setup()

    args = Namespace(**kwargs)

    aligner = _pretrained_aligner(args)

    try:
        aligner.align()
        _export_files_to_database(aligner.files)
        aligner.export_files(args.output_directory)
    except Exception:
        aligner.dirty = True
        raise
    finally:
        aligner.cleanup()


def _mfa_setup():
    check_third_party()
    hooks = command_line.mfa.ExitHooks()
    hooks.hook()
    atexit.register(hooks.history_save_handler)

    from colorama import init

    init()


def _export_files_to_database(files, database):
    total = len(files)
    with SQLiteDB(database) as _:
        for file in tqdm(
            files, desc="Inserting alignment files into database", total=total
        ):
            clips = file.aligned_data["clips"]

            for loc, interval in enumerate(clips["words"]):
                pass

            for interval in clips["phones"]:
                pass


def _pretrained_aligner(args):
    command_line.align.validate_args(args)
    aligner = PretrainedAligner(
        acoustic_model_path=args.acoustic_model_path,
        corpus_directory=args.corpus_directory,
        dictionary_path=args.dictionary_path,
        temporary_directory=args.temporary_directory,
        **PretrainedAligner.parse_parameters(args.config_path, args),
    )
    return aligner


def _word_alignment():
    return
