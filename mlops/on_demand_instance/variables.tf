variable "availability_zone" {
  default     = "us-east-1a"
  description = "The availability zone to run the instance"
  type        = string
}

variable "instance_type" {
  default     = "p2.xlarge"
  description = "The EC2 instance type to use"
  type        = string
}

variable "key_name" {
  description = "The name to associate with the public key"
  type        = string
}

variable "public_key" {
  description = "The RSA public key to associate with the EC2 instance"
  sensitive   = true
  type        = string
}

variable "region" {
  default     = "us-east-1"
  description = "AWS region"
  type        = string
}

variable "tag_name" {
  default     = null
  description = "Tag name to put on instances created by this terraform"
  type        = string
}
