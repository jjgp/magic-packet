import atexit
from argparse import Namespace

import click
from montreal_forced_aligner import command_line
from montreal_forced_aligner.alignment import PretrainedAligner
from montreal_forced_aligner.config import get_temporary_directory
from montreal_forced_aligner.utils import check_third_party


@click.command()
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

    check_third_party()
    hooks = command_line.mfa.ExitHooks()
    hooks.hook()
    atexit.register(hooks.history_save_handler)

    from colorama import init

    init()

    args = Namespace(**kwargs)
    command_line.align.validate_args(args)
    aligner = PretrainedAligner(
        acoustic_model_path=args.acoustic_model_path,
        corpus_directory=args.corpus_directory,
        dictionary_path=args.dictionary_path,
        temporary_directory=args.temporary_directory,
        **PretrainedAligner.parse_parameters(args.config_path, args),
    )

    try:
        aligner.align()
        aligner.export_files(args.output_directory)
    except Exception:
        aligner.dirty = True
        raise
    finally:
        aligner.cleanup()
