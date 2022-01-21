#!/bin/bash

cd /home/ubuntu

# Clone repository
git clone "https://github.com/jjgp/magic-packet"
chown -R ubuntu: magic-packet

# Install magic-packet dependencies
pushd magic-packet
conda env create -y -f environments/ubuntu_x86_64/magic-packet.yml
popd

# Clone howl repository
git clone "https://github.com/castorini/howl.git"
chown -R ubuntu: magic-packet
