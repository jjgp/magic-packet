import argparse
from collections import defaultdict

from magic_packet.cli import common_voice, train

_ALIASES = defaultdict(list, {"common_voice": ["cv"]})


def main():
    parser = argparse.ArgumentParser(description="the magic packet cli")
    subparsers = parser.add_subparsers(required=True)

    for module in (common_voice, train):
        name = module.__name__.split(".")[-1]
        subparser = subparsers.add_parser(name, aliases=_ALIASES[name])
        module.add_to_parser(subparser)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
