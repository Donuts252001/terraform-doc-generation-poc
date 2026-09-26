terraform {
  backend "s3" {
    bucket = "terraform-state-bucket"
    key    = "terraform/dev/terraform.tfstate"
    region = var.region
  }
}
