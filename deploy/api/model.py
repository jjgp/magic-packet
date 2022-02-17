# NOTE: much of this code is adapted from https://github.com/harvard-edge/multilingual_kws  # noqa

import glob
import logging

import absl
import tensorflow as tf

tf.config.set_visible_devices([], "GPU")  # disable GPU

from absl import logging as absl_logging

absl_logging.set_verbosity(absl.logging.ERROR)

from multilingual_kws.embedding import input_data  # noqa

AUTOTUNE = tf.data.experimental.AUTOTUNE
BATCH_SIZE = 64
CATEGORIES = 3  # silence + unknown + target_keyword
EPOCHS = 4
LEARNING_RATE = 1e-3
MODEL_SETTTINGS = input_data.standard_microspeech_model_settings(label_count=CATEGORIES)


def predict(audio, model_path):
    spec = input_data.to_micro_spectrogram(MODEL_SETTTINGS, audio)
    single_batch = tf.expand_dims(
        spec[..., tf.newaxis], axis=0
    )  # input shape should be (1, 49, 40, 1)
    model = tf.keras.models.load_model(model_path)
    return model.predict(single_batch)


def train(
    background_noise_path, embedding_path, samples_path, save_path, unknown_files_path
):
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
            tf.keras.layers.Dense(18, activation="tanh"),
            tf.keras.layers.Dense(
                CATEGORIES, activation="softmax"
            ),  # silence + unknown + target_keyword
        ]
    )
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
        metrics=["accuracy"],
    )

    dataset = train_dataset(background_noise_path, samples_path, unknown_files_path)
    history = model.fit(dataset, steps_per_epoch=BATCH_SIZE, epochs=EPOCHS)
    model.save(save_path)
    return history.history


def train_dataset(background_noise_path, samples_path, unknown_files_path):
    unknown_files_txt = f"{unknown_files_path}/unknown_files.txt"
    unknown_files = []
    with open(unknown_files_txt, "r") as fobj:
        for wav in fobj.read().splitlines():
            unknown_files.append(f"{unknown_files_path}/{wav}")

    audio_dataset = input_data.AudioDataset(
        model_settings=MODEL_SETTTINGS,
        commands=[
            "_KEYWORD_"
        ],  # normally this would be the actual keyword. using a sentinel server-side.
        background_data_dir=background_noise_path,
        unknown_files=unknown_files,
        unknown_percentage=50.0,
        spec_aug_params=input_data.SpecAugParams(percentage=80),
    )

    samples = glob.glob(f"{samples_path}/*.wav")
    init_train_ds = audio_dataset.init_single_target(
        AUTOTUNE, samples, is_training=True
    )
    return init_train_ds.shuffle(buffer_size=1000).repeat().batch(BATCH_SIZE)
