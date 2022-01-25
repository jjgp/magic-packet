from tensorflow.keras.layers import Input

from . import models


def add_to_parser(parser):
    parser.description = "model training"
    parser.set_defaults(func=train)
    parser.add_argument("--dataset", choices=["speech_commands"], default="")
    parser.add_argument(
        "--vocab",
        nargs="+",
        default=["hey", "fire", "fox"],
        help="the working directory to write intermediate artifacts",
    )

    subparsers = parser.add_subparsers(required=True)
    models.add_to_subparsers(subparsers)


def train(args):
    model = args.model(args)
    model = model(Input(shape=(124, 13, 1)))
    model.summary()
