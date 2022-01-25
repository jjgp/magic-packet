from tensorflow.keras.layers import Input

from . import models


def add_to_parser(parser):
    parser.description = "model training"
    parser.set_defaults(func=train)

    subparsers = parser.add_subparsers(required=True)
    models.add_to_subparsers(subparsers)


def train(args):
    model = args.model(args)
    model = model(Input(shape=(124, 13, 1)))
    model.summary()
