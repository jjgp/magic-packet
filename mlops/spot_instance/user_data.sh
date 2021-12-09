#!/usr/bin/env bash

# Note that this script assumes:
# - The device name is /dev/sdh
# - The user is ubuntu

# Attach to the EBS volume
availability_zone="${availability_zone}"
instance_id=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)

aws ec2 attach-volume \
	--region $region \
    --volume-id $volume_id \
	--instance-id $instance_id \
    --device /dev/sdh

aws ec2 wait volume-in-use --volume-ids $volume_id

# Mount the volume
mkdir /data
mount /dev/xvdh /data
chown -R ubuntu: /data

cd /home/ubuntu
git clone https://github.com/jjgp/magic-packet
chown -R ubuntu: magic-packet

# TODO: start Jupyter server
