# AWS Infrastructure Documentation

## Metadata
- **Documentation by:** Terraform
- **Updated date:** 2026-10-09 07:03:30 UTC
- **Commit ID:** 809efd4
- **Environment:** `dev`
- **AWS Region:** `eu-west-1` (derived from resource ARNs)

---

## Infrastructure Overview
This document logs the targeted changes, creations, and deletions of resources in the AWS infrastructure based on the latest Terraform plan execution. 

Summary of changes:
- **Created Resources:** 1 Internet Gateway, 1 ECS Cluster, 5 S3 Buckets (along with 5 Versioning configurations).
- **Deleted Resources:** 1 DB Subnet Group, 1 RDS Security Group.
- No-op resources (VPC, Subnets, and ECS Security Group) are excluded from this update.

---

## VPC and Networking

### Internet Gateways

#### `aws_internet_gateway.igw`
- **Resource Type:** `aws_internet_gateway`
- **Resource Name:** `igw`
- **Action:** **Create**
- **Location:** VPC `vpc-0af0069b699c8f61d` (Region `eu-west-1`)
- **Purpose:** Connects the VPC to the internet, enabling public routing.
- **Important Settings:**
  - `vpc_id`: `vpc-0af0069b699c8f61d`
  - Tags: 
    - `Name`: `dev-igw`

---

## Security Groups

### Deleted Security Groups

#### `aws_security_group.rds_sg`
- **Resource Type:** `aws_security_group`
- **Resource Name:** `rds_sg`
- **Action:** **Delete**
- **Location:** VPC `vpc-0af0069b699c8f61d`
- **Purpose:** Formerly secured RDS traffic.
- **Previous Configuration:**
  - Security Group Name: `dev-rds-sg`
  - Ingress: Allowed TCP traffic on port `5432` from ECS Security Group `sg-0c4c9fc5e8d1ff327`.
  - Egress: None.

---

## Compute Resources

### ECS Clusters

#### `aws_ecs_cluster.main_ecs2`
- **Resource Type:** `aws_ecs_cluster`
- **Resource Name:** `main_ecs2`
- **Action:** **Create**
- **Location:** Region `eu-west-1`
- **Purpose:** New ECS cluster to deploy and orchestrate containerized workloads.
- **Important Settings:**
  - `name`: `dev-cluster2`
  - Container Insights: `enabled`
  - Tags:
    - `Environment`: `dev`
    - `ManagedBy`: `Terraform`

---

## Storage Resources

### S3 Buckets

#### `aws_s3_bucket.uploads_bucket`
- **Resource Type:** `aws_s3_bucket` / `aws_s3_bucket_versioning`
- **Resource Name:** `uploads_bucket`
- **Action:** **Create**
- **Purpose:** Primary bucket for system uploads with full object versioning protection.
- **Important Settings:**
  - `bucket_prefix`: `dev-uploads-bucket-`
  - Versioning Status: **Enabled**
  - Tags:
    - `Name`: `dev-uploads`
    - `Environment`: `dev`
    - `ManagedBy`: `Terraform`

#### `aws_s3_bucket.uploads_bucket_2`
- **Resource Type:** `aws_s3_bucket` / `aws_s3_bucket_versioning`
- **Resource Name:** `uploads_bucket_2`
- **Action:** **Create**
- **Purpose:** Secondary uploads storage.
- **Important Settings:**
  - `bucket_prefix`: `dev-uploads-bucket-2`
  - Versioning Status: **Disabled**
  - Tags:
    - `Name`: `dev-uploads-2`
    - `Environment`: `dev`
    - `ManagedBy`: `Terraform`

#### `aws_s3_bucket.uploads_bucket_3`
- **Resource Type:** `aws_s3_bucket` / `aws_s3_bucket_versioning`
- **Resource Name:** `uploads_bucket_3`
- **Action:** **Create**
- **Purpose:** Tertiary uploads storage.
- **Important Settings:**
  - `bucket_prefix`: `dev-uploads-bucket-3`
  - Versioning Status: **Disabled**
  - Tags:
    - `Name`: `dev-uploads-3`
    - `Environment`: `dev`
    - `ManagedBy`: `Terraform`

#### `aws_s3_bucket.uploads_bucket_4`
- **Resource Type:** `aws_s3_bucket` / `aws_s3_bucket_versioning`
- **Resource Name:** `uploads_bucket_4`
- **Action:** **Create**
- **Purpose:** Additional uploads bucket.
- **Important Settings:**
  - `bucket_prefix`: `dev-uploads-bucket-4`
  - Versioning Status: **Disabled**
  - Tags:
    - `Name`: `dev-uploads-4`
    - `Environment`: `dev`
    - `ManagedBy`: `Terraform`

#### `aws_s3_bucket.uploads_bucket_6`
- **Resource Type:** `aws_s3_bucket` / `aws_s3_bucket_versioning`
- **Resource Name:** `uploads_bucket_6`
- **Action:** **Create**
- **Purpose:** Additional uploads bucket with active version control.
- **Important Settings:**
  - `bucket_prefix`: `dev-uploads-bucket-6`
  - Versioning Status: **Enabled**
  - Tags:
    - `Name`: `dev-uploads-6`
    - `Environment`: `dev`
    - `ManagedBy`: `Terraform`

---

## Databases

### Deleted Database Components

#### `aws_db_subnet_group.main_db_subnet_grp`
- **Resource Type:** `aws_db_subnet_group`
- **Resource Name:** `main_db_subnet_grp`
- **Action:** **Delete**
- **Location:** VPC `vpc-0af0069b699c8f61d`
- **Purpose:** Provided subnets for RDS DB instance deployments.
- **Previous Configuration:**
  - Subnet Group Name: `dev-db-subnet-group`
  - Subnet IDs associated: `subnet-077bdbd7558c71e67` and `subnet-07af81f6985379253`

---

## Resource Relationships & Connection Details
- **Internet Access:** The newly created `aws_internet_gateway.igw` (`dev-igw`) associates with the VPC `vpc-0af0069b699c8f61d` to provide outer network access capability.
- **RDS & DB Subnets Deletion:** The deletion of `aws_db_subnet_group.main_db_subnet_grp` (`dev-db-subnet-group`) and `aws_security_group.rds_sg` (`dev-rds-sg`) removes database connectivity layers from VPC `vpc-0af0069b699c8f61d`. Under previous associations, RDS accepted ingress requests on port `5432` from the ECS security group `sg-0c4c9fc5e8d1ff327`.