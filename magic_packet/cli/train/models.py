from magic_packet.models import resnet8


def add_to_subparsers(subparsers):
    subparser = subparsers.add_parser("resnet8")
    resnet8.add_to_parser(subparser)
