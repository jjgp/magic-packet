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

data "aws_availability_zones" "available" {}

locals {
  availability_zone = data.aws_availability_zones.available.names[0]
  # Acronym for magic packet spot instance
  tag_name = "mpsi"
}

resource "aws_vpc" "mpsi_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name = local.tag_name
  }
}

resource "aws_internet_gateway" "mpsi_internet_gateway" {
  vpc_id = aws_vpc.mpsi_vpc.id

  tags = {
    Name = local.tag_name
  }
}

resource "aws_route_table" "mpsi_route_table" {
  vpc_id = aws_vpc.mpsi_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.mpsi_internet_gateway.id
  }

  tags = {
    Name = local.tag_name
  }
}

resource "aws_subnet" "mpsi_subnet" {
  availability_zone = local.availability_zone
  cidr_block        = "10.0.1.0/24"
  vpc_id            = aws_vpc.mpsi_vpc.id

  tags = {
    Name = local.tag_name
  }
}

resource "aws_route_table_association" "mpsi_route_table_association" {
  subnet_id      = aws_subnet.mpsi_subnet.id
  route_table_id = aws_route_table.mpsi_route_table.id
}

resource "aws_security_group" "mpsi_security_group" {
  vpc_id = aws_vpc.mpsi_vpc.id

  ingress {
    protocol    = "tcp"
    from_port   = 22
    to_port     = 22
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    protocol    = "tcp"
    from_port   = 8888
    to_port     = 8888
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = local.tag_name
  }
}

resource "aws_key_pair" "mpsi_key_pair" {
  key_name   = var.key_name
  public_key = var.public_key

  tags = {
    Name = local.tag_name
  }
}

resource "aws_spot_instance_request" "mpsi_spot_instance_request" {
  ami                         = var.ami
  associate_public_ip_address = true
  availability_zone           = local.availability_zone
  instance_type               = var.instance_type
  key_name                    = var.key_name
  subnet_id                   = aws_subnet.mpsi_subnet.id
  vpc_security_group_ids      = [aws_security_group.mpsi_security_group.id]

  tags = {
    Name = local.tag_name
  }
}
