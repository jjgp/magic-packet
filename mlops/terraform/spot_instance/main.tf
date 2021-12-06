terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.68"
    }
  }
}

locals {
  tag_name = "magic_packet_spot_instance"
}

provider "aws" {
  region = var.region
}

# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/key_pair
resource "aws_key_pair" "key_pair" {
  key_name   = var.key_name
  public_key = var.public_key

  tags = {
    Name = local.tag_name
  }
}

# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/spot_instance_request
resource "aws_spot_instance_request" "instance_request" {
  # Currently the AMI and instance may only work in eu-west-1
  ami           = "ami-015b1508a2ff2c65a"
  instance_type = "t2.micro"
  key_name      = var.key_name

  tags = {
    Name = local.tag_name
  }
}
