terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.68"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 3.1"
    }
  }
}

provider "aws" {
  region = var.region
}

data "tls_public_key" "public_key" {
  private_key_pem = file(var.private_key_pem)
}

resource "aws_key_pair" "key_pair" {
  key_name   = var.key_name
  public_key = data.tls_public_key.key_pair.public_key_openssh
}

resource "aws_spot_instance_request" "cheap_worker" {
  ami = "ami-015b1508a2ff2c65a"
  # https://aws.amazon.com/ec2/spot/pricing/
  instance_type = "t2.micro"
  key_name      = var.key_name

  tags = {
    Name = "cheap_worker"
  }
}