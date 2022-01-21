#!/bin/bash

instance_id=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)

# Necessary if the AWS CLI must be installed
apt-get update && apt-get install -y unzip

# Install AWS CLI
if ! command -v aws &> /dev/null; then
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    ./aws/install
    rm -rf awscliv2.zip aws
fi

# Attach to the EBS volume
aws ec2 attach-volume \
	--region "${region}" \
    --volume-id "${volume_id}" \
	--instance-id $instance_id \
    --device /dev/sdh

aws ec2 wait volume-in-use \
    --volume-ids "${volume_id}" \
    --filters "Name=attachment.status,Values=attached"

# Format and mount the volume
mkfs -t xfs /dev/xvdh
mkdir /data
mount /dev/xvdh /data
chown -R ubuntu: /data

cd /home/ubuntu

# Clone magic-packet repository
git clone "https://github.com/jjgp/magic-packet"
chown -R ubuntu: magic-packet

# Clone howl repository
git clone "https://github.com/castorini/howl.git"
chown -R ubuntu: howl
