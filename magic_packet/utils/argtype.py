import argparse
import os
import tarfile as tfile


def tarfile(arg):
    arg = path(arg)
    if not tfile.is_tarfile(arg):
        raise argparse.ArgumentTypeError(f"{arg} is not a tarfile")
    return arg


def path(arg):
    abspath = os.path.abspath(arg)
    if not os.path.exists(abspath):
        raise argparse.ArgumentTypeError(f"{arg} does not exist")
    return arg
