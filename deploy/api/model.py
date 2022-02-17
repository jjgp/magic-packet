import logging

import absl
import tensorflow as tf
from absl import logging as absl_logging

absl_logging.set_verbosity(absl.logging.ERROR)

from multilingual_kws.embedding import input_data  # noqa

AUTOTUNE = tf.data.experimental.AUTOTUNE
BATCH_SIZE = 64
CATEGORIES = 3  # silence + unknown + target_keyword
EPOCHS = 4
LEARNING_RATE = 1e-3


def train(background_noise_path, embedding_path, samples_path, unknown_files_path):
    tf.get_logger().setLevel(logging.ERROR)
    base_model = tf.keras.models.load_model(embedding_path)
    tf.get_logger().setLevel(logging.INFO)

    embedding = tf.keras.models.Model(
        name="embedding_model",
        inputs=base_model.inputs,
        outputs=base_model.get_layer(name="dense_2").output,
    )
    embedding.trainable = False

    model = tf.keras.models.Sequential(
        [
            embedding,
            tf.keras.layers.Dense(units=18, activation="tanh"),
            tf.keras.layers.Dense(
                units=CATEGORIES, activation="softmax"
            ),  # silence + unknown + target_keyword
        ]
    )
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
        metrics=["accuracy"],
    )


def train_dataset(background_noise_path, samples_path, unknown_files_path):
    pass
