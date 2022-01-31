import os

import click

from .common_voice import common_voice
from .train import train


@click.group()
@click.option("--tf-log-level", type=click.Choice(["0", "1", "2", "3"]), default="2")
def magicpkt(tf_log_level):
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = tf_log_level


magicpkt.add_command(common_voice)
magicpkt.add_command(train)


if __name__ == "__main__":
    magicpkt()
