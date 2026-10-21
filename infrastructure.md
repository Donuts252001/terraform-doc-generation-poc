# AWS Infrastructure Documentation

- **Infrastructure overview**: Updated development infrastructure including VPC networking, subnets, internet gateway, security groups, ECS cluster, PostgreSQL database instance, DB subnet group, and S3 upload buckets with versioning.
- **Documentation by**: Terraform
- **Updated date**: 2026-10-21 07:13:58 UTC
- **Commit ID**: feedf56
- **Environment**: dev
- **AWS region**: eu-central-1

---

## VPC and Networking

### VPC (`aws_vpc.main_vpc`)
- **Resource Type**: `aws_vpc`
- **Resource Name**: `main_vpc`
- **Location**: `eu-central-1`
- **Purpose**: Provides the foundational virtual private cloud network for the development environment.
- **Important Settings**:
  - CIDR Block: `10.0.0.0/16`
  - Enable DNS Hostnames: `true`
  - Enable DNS Support: `true`
  - Instance Tenancy: `default`
- **Dependencies/Relationships/Connections**: Acts as the parent network resource for subnets, internet gateway, and security groups.

---

## Subnets

### Public Subnet (`aws_subnet.public-subnet`)
- **Resource Type**: `aws_subnet`
- **Resource Name**: `public-subnet`
- **Location**: `eu-west-1a`
- **Purpose**: Provides a public subnet with automated public IP assignment for external-facing resources.
- **Important Settings**:
  - CIDR Block: `10.0.1.0/24`
  - Map Public IP on Launch: `true`
  - Availability Zone: `eu-west-1a`
- **Dependencies/Relationships/Connections**: Associated with `aws_vpc.main_vpc`.

### Private Subnet (`aws_subnet.private-subnet`)
- **Resource Type**: `aws_subnet`
- **Resource Name**: `private-subnet`
- **Location**: `eu-west-1b`
- **Purpose**: Provides a private subnet without public IP assignment for backend resources.
- **Important Settings**:
  - CIDR Block: `10.0.10.0/24`
  - Map Public IP on Launch: `false`
  - Availability Zone: `eu-west-1b`
- **Dependencies/Relationships/Connections**: Associated with `aws_vpc.main_vpc`.

### DB Subnet Group (`aws_db_subnet_group.main_db_subnet_grp`)
- **Resource Type**: `aws_db_subnet_group`
- **Resource Name**: `dev-db-subnet-group`
- **Location**: `eu-central-1`
- **Purpose**: Groups subnets together for RDS database deployment.
- **Important Settings**:
  - Name: `dev-db-subnet-group`
- **Dependencies/Relationships/Connections**: Associated with the main VPC and used by the PostgreSQL database instance.

---

## Internet/NAT Gateways

### Internet Gateway (`aws_internet_gateway.igw`)
- **Resource Type**: `aws_internet_gateway`
- **Resource Name**: `igw`
- **Location**: `eu-central-1`
- **Purpose**: Enables access to the internet for resources within the VPC.
- **Important Settings**:
  - Name Tag: `dev-igw`
- **Dependencies/Relationships/Connections**: Attached to `aws_vpc.main_vpc`.

---

## Security Groups

### ECS Security Group (`aws_security_group.ecs_sg`)
- **Resource Type**: `aws_security_group`
- **Resource Name**: `ecs_sg`
- **Location**: `eu-central-1`
- **Purpose**: Controls network traffic for ECS container tasks.
- **Important Settings**:
  - Name: `dev-ecs-sg`
  - Ingress: TCP port `3000` from CIDR block `10.0.0.0/16`
  - Egress: All traffic allowed (`0.0.0.0/0`, port `0`, protocol `-1`)
- **Dependencies/Relationships/Connections**: Associated with `aws_vpc.main_vpc`.

### RDS Security Group (`aws_security_group.rds_sg`)
- **Resource Type**: `aws_security_group`
- **Resource Name**: `rds_sg`
- **Location**: `eu-central-1`
- **Purpose**: Controls network traffic for the RDS database instance.
- **Important Settings**:
  - Name: `dev-rds-sg`
  - Ingress: TCP port `5432`
- **Dependencies/Relationships/Connections**: Associated with `aws_vpc.main_vpc` and protects `aws_db_instance.postgres`.

---

## Compute Resources

### ECS Cluster (`aws_ecs_cluster.main_ecs2`)
- **Resource Type**: `aws_ecs_cluster`
- **Resource Name**: `main_ecs2`
- **Location**: `eu-central-1`
- **Purpose**: Provides a container orchestration cluster for running ECS services in the development environment.
- **Important Settings**:
  - Name: `dev-cluster2`
  - Settings: Container Insights enabled (`enabled`)
- **Dependencies/Relationships/Connections**: Manages containerized application workloads.

---

## Storage Resources

### S3 Upload Buckets (`aws_s3_bucket.uploads_bucket`, `aws_s3_bucket.uploads_bucket_2`, `aws_s3_bucket.uploads_bucket_3`, `aws_s3_bucket.uploads_bucket_4`)
- **Resource Type**: `aws_s3_bucket`
- **Resource Names**: `dev-uploads`, `dev-uploads-2`, `dev-uploads-3`, `dev-uploads-4`
- **Location**: `eu-central-1`
- **Purpose**: Provides object storage buckets for handling file uploads in the development environment.
- **Important Settings**:
  - Bucket Prefixes: `dev-uploads-bucket-`, `dev-uploads-bucket-2`, `dev-uploads-bucket-3`, `dev-uploads-bucket-4`
  - Force Destroy: `false`
- **Dependencies/Relationships/Connections**: Configured with individual S3 bucket versioning resources (`aws_s3_bucket_versioning`).

### S3 Bucket Versioning (`aws_s3_bucket_versioning.uploads_bucket`, `aws_s3_bucket_versioning.uploads_bucket_2`, `aws_s3_bucket_versioning.uploads_bucket_3`, `aws_s3_bucket_versioning.uploads_bucket_4`)
- **Resource Type**: `aws_s3_bucket_versioning`
- **Resource Names**: Corresponding versioning configurations for the S3 upload buckets.
- **Location**: `eu-central-1`
- **Purpose**: Manages versioning states for the S3 upload buckets.
- **Important Settings**:
  - `uploads_bucket` Status: `Enabled`
  - `uploads_bucket_2`, `uploads_bucket_3`, `uploads_bucket_4` Status: `Disabled`
- **Dependencies/Relationships/Connections**: Attached directly to their respective `aws_s3_bucket` resources.

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
  - Protected by Security Group `aws_security_group.rds_sg` (`dev-rds-sg`), which allows incoming traffic on port 5432.
- **Desired and Current Capacity/Instances**: 
  - Instance Class: `db.t3.micro` (Single instance, non-Multi-AZ deployment).