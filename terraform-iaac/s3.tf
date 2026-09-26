resource "aws_s3_bucket" "uploads_bucket" {
  bucket_prefix = "${var.environment}-uploads-bucket-"

  tags = {
    Name        = "${var.environment}-uploads"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_s3_bucket_versioning" "uploads_bucket" {
  bucket = aws_s3_bucket.uploads_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket" "uploads_bucket_2" {
  bucket_prefix = "${var.environment}-uploads-bucket-2"

  tags = {
    Name        = "${var.environment}-uploads-2"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_s3_bucket_versioning" "uploads_bucket_2" {
  bucket = aws_s3_bucket.uploads_bucket_2.id

  versioning_configuration {
    status = "Disabled"
  }
}