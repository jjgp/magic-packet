variable "ami" {
  default     = "ami-015b1508a2ff2c65a"
  description = "The AMI to use for the instance"
  type        = string
}

variable "availability_zone" {
  description = "The availability zone to run the instance"
  type        = string
}

variable "instance_type" {
  description = "The EC2 instance type to use"
  type        = string
}

variable "key_name" {
  description = "The name to associate with the public key"
  type        = string
}

variable "public_key" {
  description = "The RSA public key to associate with the EC2 instance"
  type        = string
  sensitive   = true
}

variable "region" {
  description = "AWS region"
  type        = string
}

variable "tag_name" {
  description = "Tag name to put on instances created by this terraform"
  type        = string
}
