#!/bin/bash

cd /home/ubuntu

# Clone magic-packet repository
git clone "https://github.com/jjgp/magic-packet"
chown -R ubuntu: magic-packet

# Clone howl repository
git clone "https://github.com/castorini/howl.git"
chown -R ubuntu: howl
