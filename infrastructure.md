# AWS Infrastructure Documentation

- Infrastructure overview
- Documentation by: Terraform
- Updated date: 2026-10-06 07:23:11 UTC
- Commit ID: 6319a16
- Environment: dev
- AWS region: eu-west-1

---

## VPC and networking

### Virtual Private Cloud (VPC)
- **Resource type:** `aws_vpc`
- **Resource name:** `main_vpc`
- **Location:** AWS Region `eu-west-1`
- **Purpose:** Core isolated networking environment for development resources.
- **Important settings:**
  - CIDR Block: `10.0.0.0/16`
  - DNS Hostnames: Enabled (`true`)
  - DNS Support: Enabled (`true`)
  - Instance Tenancy: `default`
  - Tags: `Name = dev-vpc`, `Environment = dev`, `ManagedBy = Terraform`

### Internet Gateway
- **Resource type:** `aws_internet_gateway`
- **Resource name:** `igw`
- **Location:** AWS Region `eu-west-1`
- **Purpose:** Provides communication between the VPC and the internet.
- **Dependencies/relationships/connections:** Attached to `aws_vpc.main_vpc`.
- **Important settings:**
  - Tags: `Name = dev-igw`

---

## Subnets

### Public Subnet
- **Resource type:** `aws_subnet`
- **Resource name:** `public-subnet`
- **Location:** Availability Zone `eu-west-1a`
- **Purpose:** Hosts public-facing resources requiring direct internet routing.
- **Dependencies/relationships/connections:** Associated with `aws_vpc.main_vpc`.
- **Important settings:**
  - CIDR Block: `10.0.1.0/24`
  - Map Public IP on Launch: Enabled (`true`)
  - Tags: `Name = dev-public-subnet`, `Type = Public`

### Private Subnet
- **Resource type:** `aws_subnet`
- **Resource name:** `private-subnet`
- **Location:** Availability Zone `eu-west-1b`
- **Purpose:** Hosts backend workloads and databases isolated from direct public internet access.
- **Dependencies/relationships/connections:** Associated with `aws_vpc.main_vpc`.
- **Important settings:**
  - CIDR Block: `10.0.10.0/24`
  - Map Public IP on Launch: Disabled (`false`)
  - Tags: `Name = dev-private-subnet`, `Type = Private`

---

## Security groups

### ECS Security Group
- **Resource type:** `aws_security_group`
- **Resource name:** `ecs_sg`
- **Location:** `aws_vpc.main_vpc`
- **Purpose:** Controls network traffic for ECS container tasks.
- **Dependencies/relationships/connections:** Associated with `aws_vpc.main_vpc`.
- **Important settings:**
  - Ingress: Port `3000` (TCP) allowed from CIDR block `10.0.0.0/16`.
  - Egress: All ports and protocols (`-1`) allowed to `0.0.0.0/0`.
  - Tags: `Name = dev-ecs-sg`

---

## Compute resources

### ECS Cluster
- **Resource type:** `aws_ecs_cluster`
- **Resource name:** `main_ecs2`
- **Location:** AWS Region `eu-west-1`
- **Purpose:** Container orchestration management for development workloads.
- **Important settings:**
  - Cluster Name: `dev-cluster2`
  - Container Insights: Enabled (`value = "enabled"`)
  - Tags: `Environment = dev`, `ManagedBy = Terraform`

---

## Storage resources

### S3 Buckets
- **Resource type:** `aws_s3_bucket`
- **Resource names:** `uploads_bucket`, `uploads_bucket_2`, `uploads_bucket_3`, `uploads_bucket_4`, `uploads_bucket_6`
- **Location:** AWS Region `eu-west-1`
- **Purpose:** Object storage for application uploads in the development environment.
- **Important settings:**
  - Bucket Prefixes & Names:
    - `aws_s3_bucket.uploads_bucket` (`dev-uploads-bucket-`, `dev-uploads`)
    - `aws_s3_bucket.uploads_bucket_2` (`dev-uploads-bucket-2`, `dev-uploads-2`)
    - `aws_s3_bucket.uploads_bucket_3` (`dev-uploads-bucket-3`, `dev-uploads-3`)
    - `aws_s3_bucket.uploads_bucket_4` (`dev-uploads-bucket-4`, `dev-uploads-4`)
    - `aws_s3_bucket.uploads_bucket_6` (`dev-uploads-bucket-6`, `dev-uploads-6`)
  - Force Destroy: `false`
  - Tags: `Environment = dev`, `ManagedBy = Terraform`, `Name = dev-uploads[-2|-3|-4|-6]`

### S3 Bucket Versioning
- **Resource types:** `aws_s3_bucket_versioning`
- **Resource names:** `uploads_bucket`, `uploads_bucket_2`, `uploads_bucket_3`, `uploads_bucket_4`, `uploads_bucket_6`
- **Purpose:** Manages versioning configurations for the corresponding S3 upload buckets.
- **Important settings:**
  - `aws_s3_bucket_versioning.uploads_bucket`: Versioning status **Enabled**
  - `aws_s3_bucket_versioning.uploads_bucket_2`: Versioning status **Disabled**
  - `aws_s3_bucket_versioning.uploads_bucket_3`: Versioning status **Disabled**
  - `aws_s3_bucket_versioning.uploads_bucket_4`: Versioning status **Disabled**
  - `aws_s3_bucket_versioning.uploads_bucket_6`: Versioning status **Enabled**

---

## Databases
*(Note: PostgreSQL RDS Instance and DB Subnet Group resources have been removed from the infrastructure configuration per the current Terraform plan.)*

---

## Resource relationships
- `aws_internet_gateway.igw` is connected to `aws_vpc.main_vpc`.
- `aws_subnet.public-subnet` and `aws_subnet.private-subnet` reside within `aws_vpc.main_vpc`.
- `aws_security_group.ecs_sg` protects resources inside `aws_vpc.main_vpc`.
- `aws_s3_bucket_versioning` resources are explicitly bound to their respective `aws_s3_bucket` resources (`uploads_bucket`, `uploads_bucket_2`, `uploads_bucket_3`, `uploads_bucket_4`, `uploads_bucket_6`).

---

## ARCHITECTURE DIAGRAM

```mermaid
graph TD
    subgraph AWS ["AWS Cloud (eu-west-1)"]
        subgraph VPC ["VPC (10.0.0.0/16)"]
            IGW["Internet Gateway (dev-igw)"]
            
            subgraph SubnetPub ["Public Subnet (10.0.1.0/24 - eu-west-1a)"]
                PubResources["Public Web Traffic / Load Balancer Entry"]
            end
            
            subgraph SubnetPriv ["Private Subnet (10.0.10.0/24 - eu-west-1b)"]
                PrivResources["Private Container Tasks / Workloads"]
            end

            SG["ECS Security Group (dev-ecs-sg)"]
        end

        ECS["ECS Cluster (dev-cluster2)"]

        subgraph S3 ["S3 Buckets"]
            B1["dev-uploads<br/>(Versioning: Enabled)"]
            B2["dev-uploads-2<br/>(Versioning: Disabled)"]
            B3["dev-uploads-3<br/>(Versioning: Disabled)"]
            B4["dev-uploads-4<br/>(Versioning: Disabled)"]
            B6["dev-uploads-6<br/>(Versioning: Enabled)"]
        end
    end

    IGW <--> VPC
    PubResources <--> IGW
    PrivResources -.-> SG
    ECS -.-> PrivResources
```