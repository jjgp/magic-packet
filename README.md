# Magic Packet

![MagicPacket](https://user-images.githubusercontent.com/3421544/154582080-25c5de07-03eb-4740-b9bf-bb3d9eb3d4ca.png)

## Getting Started

`conda` environments and package dependency scripts/files are available in the _environment_ directory.
The files provide dependency setup for the _magic_packet_ module as well as working with the _mlops_ or
_notebooks_ directories.

An example of setting up a Mac device with an M1 processor:

```shell
% brew bundle --no-lock --file environment/m1/Brewfile
% conda env create -f environment/m1/environment.yml
```

_magic_packet_ module development may also be supported using the _.devcontainer_, requirements files, or `setup.py`.

## Repository Structure

The _magic_packet_ directory contains the CLI and the _magic_packet_ package. The _data_ directory is a
_work in progress_ for processing the Mozilla Common Voice dataset into aligned audio files. The _deploy_
directory contains a React client, FastAPI server, and Elastic Beanstalk configuration demonstrating the
use of embedding models for custom wake word detection. The _docker_ directory contains the Dockerfiles
to support _magic_packet_ and _deploy_ development. The _mlops_ directory contains notebooks and terraform
code to deploy EC2 instances on AWS. The _notebooks_ directory contains notebooks demonstrating a few models
for wake word detection.
