import tensorflow_datasets as tfds

from . import mini_speech_commands


def load(name, splits, shuffle_files=True, with_info=True):
    return tfds.load(
        name, split=splits, shuffle_files=shuffle_files, with_info=with_info
    )


__all__ = ["load", "mini_speech_commands"]
