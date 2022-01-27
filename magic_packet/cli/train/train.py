import click
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Input
from tensorflow.keras.losses import BinaryCrossentropy, SparseCategoricalCrossentropy
from tensorflow.keras.optimizers import Adam

from magic_packet import datasets, features


@click.group()
@click.option(
    "-d",
    "--dataset",
    type=click.Choice(["mini_speech_commands", "speech_commands"]),
    default="mini_speech_commands",
)
@click.option(
    "-s",
    "--split",
    multiple=True,
    default=["train[:80%]", "train[80%:90%]", "train[90%:]"],
)
@click.option("-e", "--epochs", type=int, default=10)
@click.option("-v", "--vocab", multiple=True)
def train(**__):
    pass


@train.resultcallback()
def train_model(partial_model, dataset, split, epochs, vocab):
    all_ds, info = datasets.load(dataset, split)
    label_names = info.features["label"].names
    train_ds, val_ds, test_ds = _preprocess_datasets(all_ds, label_names, vocab)

    for mfcc, _ in train_ds.take(1):
        input_shape = mfcc.shape

    inputs = Input(shape=input_shape)
    model = partial_model(inputs)
    model.summary()

    # TODO: may need to modify loss and metrics for class distributions
    n_outputs = partial_model.keywords["n_outputs"]
    loss = (
        SparseCategoricalCrossentropy(from_logits=True)
        if n_outputs > 1
        else BinaryCrossentropy(from_logits=True)
    )
    model.compile(optimizer=Adam(), loss=loss, metrics=["accuracy"])

    _fit(model, train_ds, val_ds, epochs)
    _evaluate(model, test_ds)
    # TODO: save model


def _evaluate(model, test_ds):
    test_audio = []
    test_labels = []

    for audio, label in test_ds:
        test_audio.append(audio.numpy())
        test_labels.append(label.numpy())

    test_audio = np.array(test_audio)
    test_labels = np.array(test_labels)

    y_pred = np.argmax(model.predict(test_audio), axis=1)
    y_true = test_labels

    test_acc = sum(y_pred == y_true) / len(y_true)
    print(f"Test set accuracy: {test_acc:.0%}")
    print(f"Confustion matrix:\n{tf.math.confusion_matrix(y_true, y_pred)}")


def _fit(model, train_ds, val_ds, epochs):
    batch_size = 64
    train_ds = train_ds.batch(batch_size)
    val_ds = val_ds.batch(batch_size)

    train_ds = train_ds.cache().prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.cache().prefetch(tf.data.AUTOTUNE)

    model.fit(train_ds, validation_data=val_ds, epochs=epochs)


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
    # TODO: cleaner way of doing this?
    # TODO: labeling logic may need to be more robust in presence of silence and other
    # noise?
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
