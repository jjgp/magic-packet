import tensorflow as tf
from tensorflow.keras.layers import Add, AvgPool2D, BatchNormalization, Conv2D, Dense
from tensorflow.keras.models import Model

_N_BLOCKS = 3
_FILTERS = 45
_POOLING = (4, 3)


def add_to_parser(parser):
    parser.description = "the resnet8 model"
    parser.add_argument("--n_blocks", type=int, default=_N_BLOCKS)
    parser.add_argument("--filters", type=int, default=_FILTERS)
    parser.add_argument("--pooling", nargs="+", type=int, default=_POOLING)
    parser.set_defaults(model=_model)


def _model(args):
    return lambda inputs, n_outputs: resnet8(
        inputs, n_outputs, args.n_blocks, args.filters, tuple(args.pooling)
    )


def resnet8(inputs, n_outputs, n_blocks=_N_BLOCKS, filters=_FILTERS, pooling=_POOLING):
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
    outputs = tf.reshape(x, shape=(-1, n_outputs))
    return Model(inputs, outputs, name="resnet8")
