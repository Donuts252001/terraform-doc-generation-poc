An updated version of the AWS infrastructure documentation is provided below, incorporating the new database resources (`aws_db_instance.postgres`, `aws_db_subnet_group.main_db_subnet_grp`, and `aws_security_group.rds_sg`) introduced in the Terraform plan, while keeping the unmodified sections intact.

# AWS Infrastructure Documentation

## Metadata
* **Documentation Tool:** Terraform
* **Updated Date:** 2026-10-09 06:02:53 UTC
* **Commit ID:** 12636ae
* **Environment:** `dev`
* **AWS Region:** `eu-west-1` (inferred from subnet availability zones)

---

## Infrastructure Overview
This document describes the planned changes to the AWS infrastructure. The deployment provisions core networking components (VPC, subnets, internet gateway, and security groups), compute clusters (Amazon ECS), object storage resources (Amazon S3 buckets with their respective versioning configurations), and database resources (Amazon RDS PostgreSQL instance, database subnet groups, and access security controls).

All resources documented below are flagged for creation (`create` action) in the Terraform plan.

---

## VPC and Networking

### VPC
#### `aws_vpc.main_vpc`
* **Resource Type:** `aws_vpc`
* **Logical Name:** `main_vpc`
* **Location:** AWS Region `eu-west-1`
* **Purpose:** Serves as the primary isolated virtual network for the `dev` environment.
* **Important Settings:**
  * **CIDR Block:** `10.0.0.0/16`
  * **Enable DNS Support:** `true`
  * **Enable DNS Hostnames:** `true`
  * **Instance Tenancy:** `default`
  * **Tags:**
    * `Name`: `dev-vpc`
    * `Environment`: `dev`
    * `ManagedBy`: `Terraform`

---

## Subnets

### Public Subnet
#### `aws_subnet.public-subnet`
* **Resource Type:** `aws_subnet`
* **Logical Name:** `public-subnet`
* **Location:** Availability Zone `eu-west-1a`
* **Purpose:** Hosts public-facing resources requiring direct routing to the Internet.
* **Important Settings:**
  * **CIDR Block:** `10.0.1.0/24`
  * **Map Public IP on Launch:** `true`
  * **Associated VPC:** `aws_vpc.main_vpc`
  * **Tags:**
    * `Name`: `dev-public-subnet`
    * `Type`: `Public`

### Private Subnet
#### `aws_subnet.private-subnet`
* **Resource Type:** `aws_subnet`
* **Logical Name:** `private-subnet`
* **Location:** Availability Zone `eu-west-1b`
* **Purpose:** Hosts isolated backend services, ECS tasks, or databases that should not be directly accessible from the public internet.
* **Important Settings:**
  * **CIDR Block:** `10.0.10.0/24`
  * **Map Public IP on Launch:** `false`
  * **Associated VPC:** `aws_vpc.main_vpc`
  * **Tags:**
    * `Name`: `dev-private-subnet`
    * `Type`: `Private`

---

## Internet/NAT Gateways

### Internet Gateway
#### `aws_internet_gateway.igw`
* **Resource Type:** `aws_internet_gateway`
* **Logical Name:** `igw`
* **Location:** Connected to `aws_vpc.main_vpc`
* **Purpose:** Allows communication between the VPC's public subnet and the internet.
* **Important Settings:**
  * **Tags:**
    * `Name`: `dev-igw`

---

## Security Groups

### ECS Security Group
#### `aws_security_group.ecs_sg`
* **Resource Type:** `aws_security_group`
* **Logical Name:** `ecs_sg`
* **Location:** Contained within `aws_vpc.main_vpc`
* **Purpose:** Controls inbound and outbound traffic for ECS container tasks.
* **Important Settings:**
  * **Ingress Rules:**
    * **Port:** `3000` (TCP)
    * **Source:** `10.0.0.0/16` (VPC CIDR boundary)
  * **Egress Rules:**
    * **Port:** All ports (`0`)
    * **Protocol:** All (`-1`)
    * **Destination:** `0.0.0.0/0` (Allow all outbound traffic)
  * **Tags:**
    * `Name`: `dev-ecs-sg`

### RDS Security Group
#### `aws_security_group.rds_sg`
* **Resource Type:** `aws_security_group`
* **Logical Name:** `rds_sg`
* **Location:** Contained within `aws_vpc.main_vpc`
* **Purpose:** Restricts inbound database traffic to allowed compute clients (such as ECS).
* **Important Settings:**
  * **Ingress Rules:**
    * **Port:** `5432` (TCP - PostgreSQL default port)
    * **Source:** Dynamic security group reference (ECS container task group)
  * **Tags:**
    * `Name`: `dev-rds-sg`

---

## Compute Resources

### ECS Cluster
#### `aws_ecs_cluster.main_ecs2`
* **Resource Type:** `aws_ecs_cluster`
* **Logical Name:** `main_ecs2`
* **Location:** `eu-west-1`
* **Purpose:** Logical grouping of tasks or services running containerized workloads in the development environment.
* **Important Settings:**
  * **Cluster Name:** `dev-cluster2`
  * **Settings:**
    * `containerInsights`: `enabled` (forces CloudWatch monitoring for cluster performance metrics)
  * **Tags:**
    * `Environment`: `dev`
    * `ManagedBy`: `Terraform`

---

## Storage Resources

### S3 Buckets & Versioning Settings

The following S3 storage buckets are to be provisioned within the `eu-west-1` region.

| Logical Name | Bucket Prefix | Force Destroy | Versioning Status | Name Tag | Environment Tag |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `aws_s3_bucket.uploads_bucket` | `dev-uploads-bucket-` | `false` | **Enabled** | `dev-uploads` | `dev` |
| `aws_s3_bucket.uploads_bucket_2` | `dev-uploads-bucket-2` | `false` | **Disabled** | `dev-uploads-2` | `dev` |
| `aws_s3_bucket.uploads_bucket_3` | `dev-uploads-bucket-3` | `false` | **Disabled** | `dev-uploads-3` | `dev` |
| `aws_s3_bucket.uploads_bucket_4` | `dev-uploads-bucket-4` | `false` | **Disabled** | `dev-uploads-4` | `dev` |
| `aws_s3_bucket.uploads_bucket_6` | `dev-uploads-bucket-6` | `false` | **Enabled** | `dev-uploads-6` | `dev` |

#### S3 Bucket Versioning Configuration Details:
* **`aws_s3_bucket_versioning.uploads_bucket`:** Configures versioning to **Enabled** on `aws_s3_bucket.uploads_bucket`.
* **`aws_s3_bucket_versioning.uploads_bucket_2`:** Configures versioning to **Disabled** on `aws_s3_bucket.uploads_bucket_2`.
* **`aws_s3_bucket_versioning.uploads_bucket_3`:** Configures versioning to **Disabled** on `aws_s3_bucket.uploads_bucket_3`.
* **`aws_s3_bucket_versioning.uploads_bucket_4`:** Configures versioning to **Disabled** on `aws_s3_bucket.uploads_bucket_4`.
* **`aws_s3_bucket_versioning.uploads_bucket_6`:** Configures versioning to **Enabled** on `aws_s3_bucket.uploads_bucket_6`.

---

## Databases

### DB Subnet Group
#### `aws_db_subnet_group.main_db_subnet_grp`
* **Resource Type:** `aws_db_subnet_group`
* **Logical Name:** `main_db_subnet_grp`
* **Purpose:** Groups subnet IDs within the VPC for RDS hosting.
* **Important Settings:**
  * **Name:** `dev-db-subnet-group`
  * **Description:** `Managed by Terraform`
  * **Tags:**
    * `Name`: `dev-db-subnet-group`

### PostgreSQL Instance
#### `aws_db_instance.postgres`
* **Resource Type:** `aws_db_instance`
* **Logical Name:** `postgres`
* **Location:** Private Subnets mapped via `dev-db-subnet-group`
* **Purpose:** Serves as the central relational database system for dev workloads.
* **Important Settings:**
  * **Engine:** `postgres` (Major Version `16`)
  * **Instance Class:** `db.t3.micro`
  * **Allocated Storage:** `20` GB
  * **Publicly Accessible:** `false`
  * **DB Subnet Group Name:** `dev-db-subnet-group`
  * **Parameter Group Name:** `default.postgres16`
  * **Skip Final Snapshot:** `true`
  * **Deletion Protection:** `false`
  * **Tags:**
    * `Name`: `dev-postgres`
    * `Environment`: `dev`
    * `ManagedBy`: `Terraform`

---

## Monitoring and Logging

* **ECS Container Insights:** Active and set to `enabled` on the `aws_ecs_cluster.main_ecs2` resource (`dev-cluster2`). This configuration triggers native collection of CPU, memory, and network usage metrics at the container and task level to Amazon CloudWatch.

---

## Resource Relationships

```
┌────────────────────────────────────────────────────────────────────────┐
│                          aws_vpc (dev-vpc)                             │
│                                                                        │
│    ┌──────────────────────────────┐      ┌────────────────────────┐    │
│    │  aws_subnet.public-subnet    │      │aws_subnet.private-sub..│    │
│    │  (10.0.1.0/24, eu-west-1a)   │      │(10.0.10.0/24, eu-west-1b)   │
│    └──────────────┬───────────────┘      └────────────┬───────────┘    │
│                   │                                   │                │
│                   ▼                                   ▼                │
│     [aws_internet_gateway.igw]              [aws_security_group.ecs_sg]│
│                                                       │ (PostgreSQL)   │
│                                                       ▼                │
│                                             [aws_security_group.rds_sg]│
│                                                       │                │
│                                                       ▼                │
│                                             [aws_db_instance.postgres] │
│                                             (dev-db-subnet-group)      │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│                        Amazon ECS Resources                            │
│                                                                        │
│      aws_ecs_cluster.main_ecs2 (dev-cluster2)                          │
│        └─ Container Insights: Enabled                                  │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│                        Amazon S3 Buckets                               │
│                                                                        │
│ ┌────────────────────────┐  ┌────────────────────────┐                 │
│ │ dev-uploads            │  │ dev-uploads-2          │                 │
│ │ (Versioning: Enabled)  │  │ (Versioning: Disabled) │                 │
│ └────────────────────────┘  └────────────────────────┘                 │
│ ┌────────────────────────┐  ┌────────────────────────┐                 │
│ │ dev-uploads-3          │  │ dev-uploads-4          │                 │
│ │ (Versioning: Disabled) │  │ (Versioning: Disabled) │                 │
│ └────────────────────────┘  └────────────────────────┘                 │
│ ┌────────────────────────┐                                             │
│ │ dev-uploads-6          │                                             │
│ │ (Versioning: Enabled)  │                                             │
│ └────────────────────────┘                                             │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Important Configuration Details
1. **IPv4 Mapping in Public Subnet:** The `aws_subnet.public-subnet` has `map_public_ip_on_launch` set to `true`. Devices deployed here will automatically receive a public IPv4 address.
2. **Container Security Boundaries:** The ECS tasks configured inside `aws_security_group.ecs_sg` are open internally to the VPC (`10.0.0.0/16`) on port `3000`. They have full internet egress capabilities to fetch external software packages, images, and API payloads.
3. **Bucket Namespace Control:** S3 Buckets utilize `bucket_prefix` rather than fixed names, enabling collision-free generation of names (appended by system-defined unique suffixes at creation time).
4. **Database Lifecycle and Snapshots:** The postgres RDS instance (`aws_db_instance.postgres`) is configured with `skip_final_snapshot = true` and `deletion_protection = false`. Deleting this database through Terraform will execute immediately without producing an automated final snapshot, appropriate for testing but requiring modification for production environments.