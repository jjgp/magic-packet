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
