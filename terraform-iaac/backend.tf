terraform {
  backend "s3" {
    bucket = "terraform-doc-generation-poc-state-bucket"
    key    = "terraform/dev/terraform.tfstate"
    region =  "eu-west-1"
  }
}
