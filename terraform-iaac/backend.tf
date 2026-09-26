terraform {
  backend "s3" {
    bucket = "terraform-doc-generation-poc-dev-state-bucket"
    key    = "terraform/dev/terraform.tfstate"
    region =  "eu-west-1"
  }
}
