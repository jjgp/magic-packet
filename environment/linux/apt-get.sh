#!/usr/bin/env bash

apt-get update && apt-get install -y \
    build-essential \
    curl \
    gnupg \
    libavcodec-extra \
    software-properties-common

curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -

apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"

apt-get update && sudo apt-get install terraform
