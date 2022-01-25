from magic_packet.cli.common_voice import createdb, download, extract


def add_to_parser(parser):
    parser.description = "subcommands to assemble the common voice dataset"
    subparsers = parser.add_subparsers(required=True)

    for module in (createdb, download, extract):
        name = module.__name__.split(".")[-1]
        subparser = subparsers.add_parser(name)
        subparser.set_defaults(func=module.main)
        module.add_to_parser(subparser)


__all__ = ["add_to_parser"]
