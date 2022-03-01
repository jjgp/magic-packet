import click

from . import align, createdb, download, extract


@click.group()
def common_voice():
    pass


common_voice.add_command(align.align)
common_voice.add_command(createdb.createdb)
common_voice.add_command(download.download)
common_voice.add_command(extract.extract)


__all__ = ["common_voice"]
