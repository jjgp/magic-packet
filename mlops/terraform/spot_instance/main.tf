terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.68"
    }
  }
}

locals {
  tag_name = "magic_packet"
}

provider "aws" {
  region = var.region
}

resource "aws_key_pair" "key_pair" {
  key_name   = var.key_name
  public_key = var.public_key

  tags = {
    Name = local.tag_name
  }
}

resource "aws_spot_instance_request" "instance_request" {
  ami           = "ami-015b1508a2ff2c65a"
  instance_type = "t2.micro"
  key_name      = var.key_name

  tags = {
    Name = local.tag_name
  }
}
