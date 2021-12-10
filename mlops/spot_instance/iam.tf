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
