from tensorflow.keras.layers import (
    Add,
    AvgPool2D,
    BatchNormalization,
    Conv2D,
    Dense,
    Flatten,
    Input,
)
from tensorflow.keras.models import Model


def resnet8(input_shape, n_labels, n_layers=6, filters=45, pooling=(4, 3)):
    """
    Some assumptions to be double checked:
    - pytorch add zero padding to maintain the dimensions. tensorflow would
    need padding as 'same' to do this.
    - tensorflow's BN parameters are slightly different and, for now, assumed
    to be unimportant.
    - howl flips the pooling dimension for their log-mel input. keeping the
    same as the paper for now (https://arxiv.org/pdf/1710.10361.pdf).
    - howl uses a torch.mean before the final output layer. unsure if this is
    of consequence.

    Implementations:
    - https://github.com/castorini/howl/blob/85c2c8b2081dd8436a616b3c235148ea3ce9d8ee/howl/model/cnn.py#L130
    - https://github.com/hyperconnect/TC-ResNet/blob/e2c449f600ea8c8604a557dab266e85460400c59/audio_nets/res.py#L29
    - https://github.com/uzh-rpg/rpg_public_dronet/blob/ac19c54bd6ac5a8fd1d220405ecf6f51af55d1f4/cnn_models.py#L10
    """  # noqa

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
    x = Flatten()(x)
    outputs = Dense(n_labels)(x)
    return Model(inputs, outputs)
