import functools

import click

from magic_packet.cli.utils.lazy_module import LazyModule

models = LazyModule("magic_packet.models")


@click.command()
@click.option("--n-outputs", type=int)
@click.option("--n-blocks", type=int, default=3)
@click.option("--filters", type=int, default=45)
@click.option("--pooling", nargs=2, type=int, default=[4, 3])
def resnet8(**kwargs):
    return functools.partial(models.resnet8, **kwargs)
