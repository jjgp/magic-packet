import argparse

from magic_packet.cli import common_voice


def main():
    parser = argparse.ArgumentParser(description="the magic packet cli")
    subparsers = parser.add_subparsers(required=True)

    parser_cv = subparsers.add_parser("common_voice", aliases=["cv"])
    common_voice.add_to_parser(parser_cv)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
