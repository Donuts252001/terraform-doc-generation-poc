# AWS Infrastructure Documentation

- **Infrastructure overview**: Incremental changes and additions to the development environment managed via Terraform, focusing on networking additions, database configuration, container orchestration, and object storage buckets.
- **Documentation by**: Terraform
- **Updated date**: 2026-10-09 10:16:09 UTC
- **Commit ID**: 5d272b4
- **Environment**: dev
- **AWS region**: eu-west-1

---

## VPC and Networking
- **Resource Type**: `aws_vpc`
- **Resource Name**: `main_vpc`
- **Location**: `eu-west-1`
- **Purpose**: Provides the foundational virtual private cloud network for the development environment.
- **Important Settings**:
  - CIDR Block: `10.0.0.0/16`
  - Instance Tenancy: `default`
  - Enable DNS Hostnames: `true`
  - Enable DNS Support: `true`
  - Tags: `Environment = dev`, `ManagedBy = Terraform`, `Name = dev-vpc`

---

## Subnets
- **Resource Type**: `aws_subnet`
- **Resource Name**: `private-subnet`
- **Location**: `eu-central-1b`
- **Purpose**: Provides private network isolation for backend database resources.
- **Important Settings**:
  - CIDR Block: `10.0.10.0/24`
  - Map Public IP on Launch: `false`
  - Tags: `Name = dev-private-subnet`, `Type = Private`
- **Dependencies/Relationships/Connections**: Associated with `aws_vpc.main_vpc`.

- **Resource Type**: `aws_subnet`
- **Resource Name**: `public-subnet`
- **Location**: `eu-central-1a`
- **Purpose**: Provides public network connectivity for inbound internet traffic.
- **Important Settings**:
  - CIDR Block: `10.0.1.0/24`
  - Map Public IP on Launch: `true`
  - Tags: `Name = dev-public-subnet`, `Type = Public`
- **Dependencies/Relationships/Connections**: Associated with `aws_vpc.main_vpc`.

---

## Internet/NAT Gateways
- **Resource Type**: `aws_internet_gateway`
- **Resource Name**: `igw`
- **Location**: `eu-west-1`
- **Purpose**: Enables internet access for resources within the VPC.
- **Important Settings**:
  - Tags: `Name = dev-igw`
- **Dependencies/Relationships/Connections**: Attached to `aws_vpc.main_vpc`.

---

## Security Groups
- **Resource Type**: `aws_security_group`
- **Resource Name**: `ecs_sg`
- **Location**: `eu-west-1`
- **Purpose**: Controls network traffic for ECS cluster container workloads.
- **Important Settings**:
  - Name: `dev-ecs-sg`
  - Ingress: TCP port `3000` allowed from CIDR block `10.0.0.0/16`.
  - Egress: All outbound traffic allowed (`0.0.0.0/0`, protocol `-1`).
  - Tags: `Name = dev-ecs-sg`
- **Dependencies/Relationships/Connections**: Attached to `aws_vpc.main_vpc`.

- **Resource Type**: `aws_security_group`
- **Resource Name**: `rds_sg`
- **Location**: `eu-west-1`
- **Purpose**: Controls network traffic for the RDS PostgreSQL database instance.
- **Important Settings**:
  - Name: `dev-rds-sg`
  - Ingress: TCP port `5432` allowed.
  - Tags: `Name = dev-rds-sg`
- **Dependencies/Relationships/Connections**: Attaches to `aws_vpc.main_vpc`.

---

## Compute Resources
- **Resource Type**: `aws_ecs_cluster`
- **Resource Name**: `main_ecs2`
- **Location**: `eu-west-1`
- **Purpose**: Manages container workloads for the secondary application cluster.
- **Important Settings**:
  - Cluster Name: `dev-cluster2`
  - Container Insights: `enabled`
  - Tags: `Environment = dev`, `ManagedBy = Terraform`
- **Desired and Current Capacity/Instances**: Managed dynamically via ECS services/tasks (Container-based compute).

---

## Storage Resources
- **Resource Types & Names**:
  - `aws_s3_bucket.uploads_bucket` (`dev-uploads`)
  - `aws_s3_bucket.uploads_bucket_2` (`dev-uploads-2`)
  - `aws_s3_bucket.uploads_bucket_3` (`dev-uploads-3`)
  - `aws_s3_bucket.uploads_bucket_4` (`dev-uploads-4`)
  - `aws_s3_bucket.uploads_bucket_6` (`dev-uploads-6`)
- **Location**: `eu-west-1`
- **Purpose**: Object storage buckets utilized for file uploads and application assets in the development environment.
- **Important Settings**:
  - Bucket Prefixes: `dev-uploads-bucket-`, `dev-uploads-bucket-2`, `dev-uploads-bucket-3`, `dev-uploads-bucket-4`, `dev-uploads-bucket-6`
  - Force Destroy: `false`
  - Versioning Configurations:
    - Enabled for `uploads_bucket` and `uploads_bucket_6` (`aws_s3_bucket_versioning`).
    - Disabled for `uploads_bucket_2`, `uploads_bucket_3`, and `uploads_bucket_4` (`aws_s3_bucket_versioning`).
  - Tags: `Environment = dev`, `ManagedBy = Terraform`, `Name = dev-uploads[-x]`
- **Dependencies/Relationships/Connections**: Associated with S3 bucket versioning resources (`aws_s3_bucket_versioning.uploads_bucket*`).

---

## Databases
- **Resource Type**: `aws_db_subnet_group`
- **Resource Name**: `main_db_subnet_grp`
- **Location**: `eu-west-1`
- **Purpose**: Groups database subnets to ensure RDS is deployed into the correct network topology.
- **Important Settings**:
  - Name: `dev-db-subnet-group`
  - Description: Managed by Terraform
  - Tags: `Name = dev-db-subnet-group`

- **Resource Type**: `aws_db_instance`
- **Resource Name**: `postgres`
- **Location**: `eu-west-1` (`dev-db-subnet-group`)
- **Purpose**: Relational database service instance running PostgreSQL for application data storage.
- **Important Settings**:
  - Identifier: `dev-postgres`
  - Engine: `postgres` (Version `16`)
  - Instance Class: `db.t3.micro`
  - Allocated Storage: `20` GB
  - Multi-AZ: `false` (Single-AZ deployment)
  - Publicly Accessible: `false`
  - Master Username: `postgres`
  - DB Subnet Group: `dev-db-subnet-group`
  - Parameter Group: `default.postgres16`
  - Backup & Deletion: Delete automated backups enabled (`true`), skip final snapshot on deletion (`true`).
  - Tags: `Environment = dev`, `ManagedBy = Terraform`, `Name = dev-postgres`
- **Dependencies/Relationships/Connections**: Depends on `aws_db_subnet_group.main_db_subnet_grp` and `aws_security_group.rds_sg`.