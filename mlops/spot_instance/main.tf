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

resource "aws_vpc" "vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name = var.tag_name
  }
}

resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = var.tag_name
  }
}

resource "aws_route_table" "route_table" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet_gateway.id
  }

  tags = {
    Name = var.tag_name
  }
}

resource "aws_subnet" "subnet" {
  availability_zone = var.availability_zone
  cidr_block        = "10.0.1.0/24"
  vpc_id            = aws_vpc.vpc.id

  tags = {
    Name = var.tag_name
  }
}

resource "aws_route_table_association" "route_table_association" {
  subnet_id      = aws_subnet.subnet.id
  route_table_id = aws_route_table.route_table.id
}

resource "aws_security_group" "security_group" {
  vpc_id = aws_vpc.vpc.id

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
    Name = var.tag_name
  }
}

resource "aws_key_pair" "key_pair" {
  key_name   = var.key_name
  public_key = var.public_key

  tags = {
    Name = var.tag_name
  }
}

resource "aws_iam_role" "iam_role" {
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })

  tags = {
    Name = var.tag_name
  }
}

resource "aws_iam_role_policy" "iam_role_policy" {
  role = aws_iam_role.iam_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ec2:AttachVolume",
          "ec2:CreateSnapshot",
          "ec2:CreateTags",
          "ec2:DescribeSnapshots",
          "ec2:DescribeVolumeStatus",
          "ec2:DescribeVolumes"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_instance_profile" "iam_instance_profile" {
  role = aws_iam_role.iam_role.id

  tags = {
    Name = var.tag_name
  }
}

resource "aws_spot_instance_request" "spot_instance_request" {
  spot_price                  = var.spot_price
  ami                         = var.ami
  wait_for_fulfillment        = true
  associate_public_ip_address = true
  availability_zone           = var.availability_zone
  iam_instance_profile        = aws_iam_instance_profile.iam_instance_profile.name
  instance_type               = var.instance_type
  key_name                    = var.key_name
  monitoring                  = true
  subnet_id                   = aws_subnet.subnet.id
  user_data = templatefile("user_data.sh", {
    availability_zone = var.availability_zone
    region            = var.region
    volume_id         = aws_ebs_volume.ebs_volume.id
  })
  vpc_security_group_ids = [aws_security_group.security_group.id]

  tags = {
    Name = var.tag_name
  }
}

resource "aws_ebs_volume" "ebs_volume" {
  availability_zone = var.availability_zone
  size              = var.volume_size
  type              = "gp2"

  tags = {
    Name = var.tag_name
  }
}
