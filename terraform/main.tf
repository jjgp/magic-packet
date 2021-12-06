terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.68"
    }
  }
}

provider "aws" {
  region = var.region
}

resource "aws_key_pair" "key_pair" {
  key_name   = var.key_name
  public_key = var.public_key

  tags = {
    Name = "magic_packet"
  }
}

resource "aws_spot_instance_request" "instance_request" {
  ami           = "ami-015b1508a2ff2c65a"
  instance_type = "t2.micro"
  key_name      = var.key_name

  tags = {
    Name = "magic_packet"
  }
}
