import tensorflow_datasets as tfds

from . import mini_speech_commands


def load(name, split, shuffle_files=True, with_info=True):
    return tfds.load(
        name, split=split, shuffle_files=shuffle_files, with_info=with_info
    )


__all__ = ["load", "mini_speech_commands"]
