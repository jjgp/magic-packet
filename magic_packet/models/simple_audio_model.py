from tensorflow.keras import layers, models


def simple_audio_model(norm_ds, input_shape, n_labels):
    """
    https://www.tensorflow.org/tutorials/audio/simple_audio#build_and_train_the_model
    """

    # Instantiate the `tf.keras.layers.Normalization` layer.
    norm_layer = layers.Normalization()
    # Fit the state of the layer to the spectrograms
    # with `Normalization.adapt`.
    norm_layer.adapt(data=norm_ds.map(map_func=lambda spec, label: spec))

    return models.Sequential(
        [
            layers.Input(shape=input_shape),
            # Downsample the input.
            layers.Resizing(32, 32),
            # Normalize.
            norm_layer,
            layers.Conv2D(32, 3, activation="relu"),
            layers.Conv2D(64, 3, activation="relu"),
            layers.MaxPooling2D(),
            layers.Dropout(0.25),
            layers.Flatten(),
            layers.Dense(128, activation="relu"),
            layers.Dropout(0.5),
            layers.Dense(n_labels),
        ]
    )
