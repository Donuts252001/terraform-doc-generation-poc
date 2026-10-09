variable "aws_region" {
  default = "eu-west-2"
}

variable "environment" {
  default = "qa"
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
