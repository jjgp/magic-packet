from . import models
from .train import train

train.add_command(models.resnet8)

__all__ = ["train"]
