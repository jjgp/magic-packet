import os

import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow_datasets.core import lazy_imports_lib


_DOWNLOAD_PATH = "https://storage.googleapis.com/download.tensorflow.org/data/mini_speech_commands.zip"  # noqa: E501
_EXAMPLES_SUBDIR = "mini_speech_commands"
_HOMEPAGE = "https://www.tensorflow.org/tutorials/audio/simple_audio#import_the_mini_speech_commands_dataset"  # noqa: E501
SAMPLE_RATE = 16000
WORDS = ["down", "go", "left", "no", "right", "stop", "up", "yes"]
UNKNOWN = "_unknown_"


class MiniSpeechCommands(tfds.core.GeneratorBasedBuilder):
    """The Mini Speech Commands dataset for keyword detection."""

    VERSION = tfds.core.Version("0.0.1")

    def _info(self):
        return tfds.core.DatasetInfo(
            builder=self,
            features=tfds.features.FeaturesDict(
                {
                    "audio": tfds.features.Audio(
                        file_format="wav", sample_rate=SAMPLE_RATE
                    ),
                    "label": tfds.features.ClassLabel(names=WORDS),
                }
            ),
            supervised_keys=("audio", "label"),
            homepage=_HOMEPAGE,
        )

    def _split_generators(self, dl_manager):
        extract_dir = dl_manager.download_and_extract(_DOWNLOAD_PATH)
        return {"train": self._generate_examples(extract_dir)}

    def _generate_examples(self, extract_dir):
        examples_subdir = os.path.join(extract_dir, _EXAMPLES_SUBDIR)
        wav_paths = tf.io.gfile.glob(examples_subdir + "/*/*")
        for wav_path in wav_paths:
            relpath, basename = os.path.split(wav_path)
            _, word = os.path.split(relpath)
            if word not in WORDS:
                continue
            example_id = f"{word}_{basename}"

            try:
                audio_segment = (
                    lazy_imports_lib.lazy_imports.pydub.AudioSegment.from_file(
                        wav_path, format="wav"
                    )
                )
                audio = np.array(audio_segment.get_array_of_samples())
                example = dict(audio=audio, label=word)
                yield example_id, example
            except lazy_imports_lib.lazy_imports.pydub.exceptions.CouldntDecodeError:
                pass
