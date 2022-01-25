import tensorflow as tf
from tensorflow.keras.layers import (
    Add,
    AvgPool2D,
    BatchNormalization,
    Conv2D,
    Dense,
    Input,
)
from tensorflow.keras.models import Model


def resnet8(input_shape, n_labels, n_layers=6, filters=45, pooling=(4, 3)):
    convargs = dict(
        filters=filters,
        kernel_size=3,
        activation="relu",
        use_bias=False,
        padding="same",
    )

    inputs = Input(shape=input_shape)
    x = Conv2D(**convargs)(inputs)
    x = AvgPool2D(pooling, padding="same")(x)

    skip = x
    for i in range(1, n_layers + 1):
        x = Conv2D(**convargs)(x)
        if i > 0 and i % 2 == 0:
            x = skip = Add()([x, skip])
        x = BatchNormalization(center=False, scale=False)(x)
    x = AvgPool2D(pool_size=x.shape[1:3], strides=1)(x)
    x = Dense(n_labels)(x)
    outputs = tf.reshape(x, shape=(-1, x.shape[3]))
    return Model(inputs, outputs)


if __name__ == "__main__":
    pass
