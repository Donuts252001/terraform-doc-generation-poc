resource "aws_security_group" "rds_sg" {
  name   = "${var.environment}-rds-sg"
  vpc_id = aws_vpc.main_vpc.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_sg.id]
  }

  tags = {
    Name = "${var.environment}-rds-sg"
  }
}

resource "aws_db_subnet_group" "main_db_subnet_grp" {
  name = "${var.environment}-db-subnet-group"

  subnet_ids = [
    aws_subnet.public-subnet.id,
    aws_subnet.private-subnet.id
  ]

  tags = {
    Name = "${var.environment}-db-subnet-group"
  }
}

resource "aws_db_instance" "postgres" {
  identifier = "${var.environment}-postgres"

  engine         = "postgres"
  engine_version = "16"

  instance_class = "db.t3.micro"

  allocated_storage = 20

  db_subnet_group_name   = aws_db_subnet_group.main_db_subnet_grp.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]

  publicly_accessible = false

  skip_final_snapshot = true
  deletion_protection = false

  tags = {
    Name        = "${var.environment}-postgres"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}