from magic_packet.cli.common_voice import download


def add_to_parser(parser):
    parser.description = "subcommands to assemble the common voice dataset"
    subparsers = parser.add_subparsers(required=True)
    parser_download = subparsers.add_parser("download")
    parser_download.set_defaults(func=download.main)
    download.add_to_parser(parser_download)


__all__ = [
    "add_to_parser",
]
