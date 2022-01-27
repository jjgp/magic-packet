import click

from .common_voice import common_voice
from .train import train


@click.group()
def magicpkt():
    pass


magicpkt.add_command(common_voice)
magicpkt.add_command(train)


if __name__ == "__main__":
    magicpkt()
