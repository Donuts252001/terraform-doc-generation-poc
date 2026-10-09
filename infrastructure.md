# AWS Infrastructure Documentation

## Infrastructure Overview
This document describes the AWS infrastructure resources managed by Terraform. The current state represents a new deployment of networking, compute, storage, and security resources in the development (`dev`) environment.

- **Documentation by:** Terraform
- **Updated date:** 2026-10-09 07:10:29 UTC
- **Commit ID:** d8f4864
- **Environment:** `dev`
- **AWS Region:** `eu-west-1` (derived from Availability Zones `eu-west-1a` and `eu-west-1b`)

---

## VPC and Networking

### VPC
*   **Resource Type:** `aws_vpc`
*   **Resource Name:** `main_vpc`
*   **Location:** `eu-west-1`
*   **Purpose:** Provides a logically isolated virtual network for hosting development resources.
*   **Important Settings:**
    *   `cidr_block`: `10.0.0.0/16`
    *   `enable_dns_support`: `true`
    *   `enable_dns_hostnames`: `true`
    *   `instance_tenancy`: `default`
    *   **Tags:**
        *   `Name`: `dev-vpc`
        *   `Environment`: `dev`
        *   `ManagedBy`: `Terraform`

---

## Subnets

### Public Subnet
*   **Resource Type:** `aws_subnet`
*   **Resource Name:** `public-subnet`
*   **Location:** `eu-west-1a`
*   **Purpose:** Houses public-facing resources requiring direct ingress and egress pathing to the internet.
*   **Important Settings:**
    *   `cidr_block`: `10.0.1.0/24`
    *   `map_public_ip_on_launch`: `true`
    *   **Tags:**
        *   `Name`: `dev-public-subnet`
        *   `Type`: `Public`
*   **Dependencies/Relationships:** Associated with `aws_vpc.main_vpc`.

### Private Subnet
*   **Resource Type:** `aws_subnet`
*   **Resource Name:** `private-subnet`
*   **Location:** `eu-west-1b`
*   **Purpose:** Houses internal application services (e.g., ECS tasks) that should not be directly accessible from the public internet.
*   **Important Settings:**
    *   `cidr_block`: `10.0.10.0/24`
    *   `map_public_ip_on_launch`: `false`
    *   **Tags:**
        *   `Name`: `dev-private-subnet`
        *   `Type`: `Private`
*   **Dependencies/Relationships:** Associated with `aws_vpc.main_vpc`.

---

## Internet/NAT Gateways

### Internet Gateway
*   **Resource Type:** `aws_internet_gateway`
*   **Resource Name:** `igw`
*   **Location:** `eu-west-1`
*   **Purpose:** Allows communication between resources in the VPC and the internet.
*   **Important Settings:**
    *   **Tags:**
        *   `Name`: `dev-igw`
*   **Dependencies/Relationships:** Attached to `aws_vpc.main_vpc`.

---

## Security Groups

### ECS Security Group
*   **Resource Type:** `aws_security_group`
*   **Resource Name:** `ecs_sg`
*   **Location:** `eu-west-1`
*   **Purpose:** Controls inbound and outbound traffic to ECS cluster tasks.
*   **Important Settings:**
    *   **Ingress Rules:**
        *   Port `3000` (TCP) allowed from the VPC CIDR range `10.0.0.0/16`.
    *   **Egress Rules:**
        *   All protocols (`-1`) and all ports allowed to egress to `0.0.0.0/0`.
    *   **Tags:**
        *   `Name`: `dev-ecs-sg`
*   **Dependencies/Relationships:** Restricts traffic to resources running inside `aws_vpc.main_vpc`.

---

## Compute Resources

### ECS Cluster
*   **Resource Type:** `aws_ecs_cluster`
*   **Resource Name:** `main_ecs2`
*   **Location:** `eu-west-1`
*   **Purpose:** Orchestrates containerized application workloads.
*   **Important Settings:**
    *   `name`: `dev-cluster2`
    *   `setting`: `containerInsights` = `enabled`
    *   **Tags:**
        *   `Environment`: `dev`
        *   `ManagedBy`: `Terraform`

---

## Storage Resources

### Uploads S3 Buckets

The infrastructure defines five distinct S3 buckets managed via name prefixes with custom versioning settings.

#### 1. Uploads Bucket 1
*   **Resource Type:** `aws_s3_bucket` & `aws_s3_bucket_versioning`
*   **Resource Name:** `uploads_bucket`
*   **Location:** `eu-west-1`
*   **Purpose:** Stores application uploads with objects versioned for backup/recovery.
*   **Important Settings:**
    *   `bucket_prefix`: `dev-uploads-bucket-`
    *   `versioning_configuration`: Status = `Enabled`
    *   **Tags:**
        *   `Name`: `dev-uploads`
        *   `Environment`: `dev`
        *   `ManagedBy`: `Terraform`

#### 2. Uploads Bucket 2
*   **Resource Type:** `aws_s3_bucket` & `aws_s3_bucket_versioning`
*   **Resource Name:** `uploads_bucket_2`
*   **Location:** `eu-west-1`
*   **Purpose:** Secondary storage bucket with versioning disabled.
*   **Important Settings:**
    *   `bucket_prefix`: `dev-uploads-bucket-2`
    *   `versioning_configuration`: Status = `Disabled`
    *   **Tags:**
        *   `Name`: `dev-uploads-2`
        *   `Environment`: `dev`
        *   `ManagedBy`: `Terraform`

#### 3. Uploads Bucket 3
*   **Resource Type:** `aws_s3_bucket` & `aws_s3_bucket_versioning`
*   **Resource Name:** `uploads_bucket_3`
*   **Location:** `eu-west-1`
*   **Purpose:** Third storage bucket with versioning disabled.
*   **Important Settings:**
    *   `bucket_prefix`: `dev-uploads-bucket-3`
    *   `versioning_configuration`: Status = `Disabled`
    *   **Tags:**
        *   `Name`: `dev-uploads-3`
        *   `Environment`: `dev`
        *   `ManagedBy`: `Terraform`

#### 4. Uploads Bucket 4
*   **Resource Type:** `aws_s3_bucket` & `aws_s3_bucket_versioning`
*   **Resource Name:** `uploads_bucket_4`
*   **Location:** `eu-west-1`
*   **Purpose:** Fourth storage bucket with versioning disabled.
*   **Important Settings:**
    *   `bucket_prefix`: `dev-uploads-bucket-4`
    *   `versioning_configuration`: Status = `Disabled`
    *   **Tags:**
        *   `Name`: `dev-uploads-4`
        *   `Environment`: `dev`
        *   `ManagedBy`: `Terraform`

#### 5. Uploads Bucket 6
*   **Resource Type:** `aws_s3_bucket` & `aws_s3_bucket_versioning`
*   **Resource Name:** `uploads_bucket_6`
*   **Location:** `eu-west-1`
*   **Purpose:** Storage bucket with versioning enabled.
*   **Important Settings:**
    *   `bucket_prefix`: `dev-uploads-bucket-6`
    *   `versioning_configuration`: Status = `Enabled`
    *   **Tags:**
        *   `Name`: `dev-uploads-6`
        *   `Environment`: `dev`
        *   `ManagedBy`: `Terraform`

---

## Monitoring and Logging

### ECS Container Insights
*   **Resource:** Configured on `aws_ecs_cluster.main_ecs2`.
*   **Purpose:** Collects, aggregates, and summarizes metrics and logs from the containerized applications.
*   **Settings:** `containerInsights` set to `enabled`.

---

## Resource Relationships

```
┌────────────────────────────────────────────────────────┐
│                      aws_vpc                           │
│                     (dev-vpc)                          │
├────────────────────────────┬───────────────────────────┤
│    aws_subnet (Public)     │    aws_subnet (Private)   │
│    (dev-public-subnet)     │    (dev-private-subnet)   │
│                            │                           │
│  [aws_internet_gateway]    │      [aws_ecs_cluster]    │
│        (dev-igw)           │       (dev-cluster2)      │
│                            │              ▲            │
│                            │              │ Associated │
│                            │              ▼            │
│                            │     [aws_security_group]  │
│                            │         (dev-ecs-sg)      │
└────────────────────────────┴───────────────────────────┘

┌────────────────────────────────────────────────────────┐
│                      S3 Buckets                        │
├────────────────────────────────────────────────────────┤
│ • dev-uploads        ──► Versioning: Enabled           │
│ • dev-uploads-2      ──► Versioning: Disabled          │
│ • dev-uploads-3      ──► Versioning: Disabled          │
│ • dev-uploads-4      ──► Versioning: Disabled          │
│ • dev-uploads-6      ──► Versioning: Enabled           │
└────────────────────────────────────────────────────────┘
```

---

## Important Configuration Details

1.  **VPC Internal Traffic Constraint:** The security group `dev-ecs-sg` only permits ingress traffic on port `3000` from sources belonging to the `10.0.0.0/16` CIDR block. Services running outside the VPC range will not be able to query container endpoints on port `3000` directly.
2.  **S3 Bucket Configuration:** All five S3 buckets are configured utilizing prefixes. True bucket names will be postfixed with random identifiers upon application of the Terraform plan. Buckets `dev-uploads` and `dev-uploads-6` have data preservation versioning **Enabled**.