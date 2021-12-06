variable "ami" {
  default     = "ami-015b1508a2ff2c65a"
  description = "The AMI to use for the instance"
  type        = string
}

variable "instance_type" {
  default     = "t2.micro"
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
