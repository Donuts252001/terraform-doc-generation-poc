# AWS Infrastructure Documentation

- **Infrastructure overview**: Addition of a new RDS PostgreSQL database instance and its associated DB subnet group within the existing development infrastructure.
- **Documentation by**: Terraform
- **Updated date**: 2026-10-09 10:17:32 UTC
- **Commit ID**: 129d8ac
- **Environment**: dev
- **AWS region**: eu-central-1

---

## Subnets

### DB Subnet Group (`aws_db_subnet_group.main_db_subnet_grp`)
- **Resource Type**: `aws_db_subnet_group`
- **Resource Name**: `dev-db-subnet-group`
- **Location**: `eu-central-1`
- **Purpose**: Groups subnets together for RDS database deployment across availability zones.
- **Important Settings**:
  - Name: `dev-db-subnet-group`
  - Subnet IDs: `subnet-0c881018565e7a3ee` (Private Subnet), `subnet-0eca3204495baf873` (Public Subnet)
- **Dependencies/Relationships/Connections**: Associated with the main VPC and used by the PostgreSQL database instance.

---

## Databases

### PostgreSQL Database Instance (`aws_db_instance.postgres`)
- **Resource Type**: `aws_db_instance`
- **Resource Name**: `dev-postgres`
- **Location**: `eu-central-1`
- **Purpose**: Provides a managed relational database service running PostgreSQL for application data storage in the development environment.
- **Important Settings**:
  - Engine: `postgres`
  - Engine Version: `16`
  - Instance Class: `db.t3.micro`
  - Allocated Storage: `20` GB
  - Database Identifier: `dev-postgres`
  - Master Username: `postgres`
  - DB Subnet Group Name: `dev-db-subnet-group`
  - Parameter Group: `default.postgres16`
  - Publicly Accessible: `false`
  - Skip Final Snapshot: `true`
  - Delete Automated Backups: `true`
- **Dependencies/Relationships/Connections**: 
  - Connected to DB Subnet Group `dev-db-subnet-group`.
  - Protected by Security Group `sg-068141e91f48dccaf` (`dev-rds-sg`), which allows incoming traffic on port 5432 from the ECS security group (`sg-0fa7a68e524a618cd`).
- **Desired and Current Capacity/Instances**: 
  - Instance Class: `db.t3.micro` (Single instance, non-Multi-AZ deployment).