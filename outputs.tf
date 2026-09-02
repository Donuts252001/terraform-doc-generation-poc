output "vpc_id" {
  value = aws_vpc.main_vpc.id
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.main_ecs.name
}

output "rds_endpoint" {
  value = aws_db_instance.postgres.endpoint
}

output "s3_bucket_name" {
  value = aws_s3_bucket.uploads_bucket.bucket
}