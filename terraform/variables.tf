variable "key_name" {
  default = "key_name"
  type    = string
}

variable "private_key_pem" {
  default = "~/.ssh/id_rsa"
  type    = string
}

variable "region" {
  default = "us-east-1"
  type    = string
}
