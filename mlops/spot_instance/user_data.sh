#!/usr/bin/env bash

availability_zone="${availability_zone}"
device_name="/dev/sdh"
device_attached_name="/dev/xvdh"
instance_id=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
mount_dir="/data"
repository_name="magic-packet"
repository_url="https://github.com/jjgp/magic-packet"
username="ubuntu"

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
    --device $device_name

aws ec2 wait volume-in-use --volume-ids "${volume_id}"

# Format and mount the volume
mkfs -t xfs $device_attached_name
mkdir $mount_dir
mount $device_attached_name $mount_dir
chown -R $username: $mount_dir

cd /home/$username
git clone $repository_url
chown -R $username: $repository_name

# TODO: start Jupyter server
