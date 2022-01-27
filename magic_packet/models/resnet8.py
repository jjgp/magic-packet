from tensorflow.keras.layers import (
    Add,
    AvgPool2D,
    BatchNormalization,
    Conv2D,
    Dense,
    Reshape,
)
from tensorflow.keras.models import Model


def resnet8(inputs, n_outputs, n_blocks=3, filters=45, pooling=(4, 3)):
    convargs = dict(
        filters=filters,
        kernel_size=3,
        activation="relu",
        use_bias=False,
        padding="same",
    )

    x = Conv2D(**convargs)(inputs)
    x = AvgPool2D(pooling, padding="same")(x)

    skip = x
    for i in range(1, 2 * n_blocks + 1):
        x = Conv2D(**convargs)(x)
        if i > 0 and i % 2 == 0:
            x = skip = Add()([x, skip])
        x = BatchNormalization(center=False, scale=False)(x)

    x = AvgPool2D(pool_size=x.shape[1:3], strides=1)(x)
    x = Dense(n_outputs)(x)
    outputs = Reshape(target_shape=(n_outputs,))(x)
    return Model(inputs, outputs)
