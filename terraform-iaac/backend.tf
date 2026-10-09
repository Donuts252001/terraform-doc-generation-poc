terraform {
  backend "s3" {
    bucket = "terraform-doc-generation-poc-dev-state-bucket"
    key    = "terraform/qa/terraform.tfstate"
    region =  "eu-west-1"
  }
}
