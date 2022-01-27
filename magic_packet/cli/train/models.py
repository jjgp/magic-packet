import functools

import click

from magic_packet import models


@click.command()
@click.option("--n_outputs", type=int)
@click.option("--n_blocks", type=int, default=3)
@click.option("--filters", type=int, default=45)
@click.option("--pooling", nargs=2, type=int, default=[4, 3])
def resnet8(**kwargs):
    return functools.partial(models.resnet8, **kwargs)
