import tensorflow as tf
from tensorflow.keras.layers import Input

from magic_packet import datasets, features

from . import models


def add_to_parser(parser):
    parser.description = "model training"
    parser.set_defaults(func=train)
    parser.add_argument(
        "-d",
        "--dataset",
        choices=["mini_speech_commands", "speech_commands"],
        default="mini_speech_commands",
    )
    parser.add_argument(
        "-s",
        "--splits",
        nargs=3,
        default=["train[:80%]", "train[80%:90%]", "train[90%:]"],
        help="the train, validation, and test splits as specified by the TFDS API",
    )
    parser.add_argument("-v", "--vocab", action="append")

    subparsers = parser.add_subparsers(required=True)
    models.add_to_subparsers(subparsers)


def train(args):
    all_ds, info = datasets.load(args.dataset, args.splits)
    label_names, vocab = info.features["label"].names, args.vocab
    train_ds, _, _ = _preprocess_datasets(all_ds, label_names, vocab)

    for mfcc, _ in train_ds.take(1):
        input_shape = mfcc.shape

    if vocab:
        n_outputs = len(vocab) + 1  # + 1 for OOV words
    else:
        n_outputs = len(label_names)

    model = args.model(args)
    inputs = Input(shape=input_shape)
    model = model(inputs, n_outputs)
    model.summary()


def _get_mfcc(example):
    audio = example["audio"]
    normalized = features.normalize(audio)
    # Add a `channels` dimension, so that the spectrogram can be used
    # as image-like input data with convolution layers (which expect
    # shape (`batch_size`, `height`, `width`, `channels`).
    mfcc = features.mfcc(normalized)[..., tf.newaxis]
    return mfcc


def _relabel_lookup_table(label_names, vocab):
    n_words = len(vocab)
    keys = tf.constant([label_names.index(word) for word in vocab], dtype=tf.int64)
    values = tf.constant(range(n_words), dtype=tf.int64)
    initializer = tf.lookup.KeyValueTensorInitializer(keys=keys, values=values)
    return tf.lookup.StaticHashTable(
        initializer=initializer, default_value=n_words  # label n_words for OOV words
    )


def _preprocess_datasets(all_ds, label_names, vocab):
    if vocab:
        table = _relabel_lookup_table(label_names, vocab)

        def get_label(example):
            return table.lookup(example["label"])

    else:

        def get_label(example):
            return example["label"]

    def get_mffc_and_label(example):
        return _get_mfcc(example), get_label(example)

    def preprocess(ds):
        return ds.map(
            map_func=get_mffc_and_label,
            num_parallel_calls=tf.data.experimental.AUTOTUNE,
        )

    return map(preprocess, all_ds)