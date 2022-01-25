from magic_packet.cli.common_voice import download, extract


def add_to_parser(parser):
    parser.description = "subcommands to assemble the common voice dataset"
    subparsers = parser.add_subparsers(required=True)

    for module in (download, extract):
        name = module.__name__.split(".")[-1]
        parser = subparsers.add_parser(name)
        parser.set_defaults(func=module.main)
        module.add_to_parser(parser)


__all__ = [
    "add_to_parser",
]
