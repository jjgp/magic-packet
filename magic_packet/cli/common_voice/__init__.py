def add_to_parser(parser):
    from . import createdb, download, extract

    parser.description = "subcommands to assemble the common voice dataset"
    subparsers = parser.add_subparsers(required=True)

    for module in (createdb, download, extract):
        name = module.__name__.split(".")[-1]
        subparser = subparsers.add_parser(name)
        module.add_to_parser(subparser)


__all__ = ["add_to_parser"]
