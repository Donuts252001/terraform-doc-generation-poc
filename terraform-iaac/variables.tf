variable "aws_region" {
  default = "eu-west-1"
}

variable "environment" {
  default = "dev"
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "access_key" {
  type = string
  sensitive = true
}

variable "secret_key" {
  type = string
  sensitive = true
}
