# AWS Infrastructure Documentation

- **Infrastructure overview:** Multi-tier containerized web application infrastructure with segregated networking and object storage.
- **Documentation by:** Terraform
- **Updated date:** 2026-10-06 08:44:38 UTC
- **Commit ID:** 15b6c6a
- **Environment:** dev
- **AWS region:** eu-west-1

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
- **Dependencies/relationships/connections:** Associated with `aws_vpc.main_vpc`.
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
  - Ingress: Port `3000` (TCP) allowed from VPC CIDR block `10.0.0.0/16`.
  - Egress: All ports and protocols (`-1`) allowed to `0.0.0.0/0` (any destination).
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
  - Force Destroy: `false`
  - Bucket Prefixes & Names:
    - `aws_s3_bucket.uploads_bucket` (Prefix: `dev-uploads-bucket-`, Tags: `Name = dev-uploads`)
    - `aws_s3_bucket.uploads_bucket_2` (Prefix: `dev-uploads-bucket-2`, Tags: `Name = dev-uploads-2`)
    - `aws_s3_bucket.uploads_bucket_3` (Prefix: `dev-uploads-bucket-3`, Tags: `Name = dev-uploads-3`)
    - `aws_s3_bucket.uploads_bucket_4` (Prefix: `dev-uploads-bucket-4`, Tags: `Name = dev-uploads-4`)
    - `aws_s3_bucket.uploads_bucket_6` (Prefix: `dev-uploads-bucket-6`, Tags: `Name = dev-uploads-6`)
  - Tags: `Environment = dev`, `ManagedBy = Terraform`

### S3 Bucket Versioning
- **Resource types:** `aws_s3_bucket_versioning`
- **Resource names:** `uploads_bucket`, `uploads_bucket_2`, `uploads_bucket_3`, `uploads_bucket_4`, `uploads_bucket_6`
- **Purpose:** Configuration to enforce or disable versioning history for objects within each S3 bucket.
- **Important settings:**
  - `aws_s3_bucket_versioning.uploads_bucket`: Status **Enabled**
  - `aws_s3_bucket_versioning.uploads_bucket_2`: Status **Disabled**
  - `aws_s3_bucket_versioning.uploads_bucket_3`: Status **Disabled**
  - `aws_s3_bucket_versioning.uploads_bucket_4`: Status **Disabled**
  - `aws_s3_bucket_versioning.uploads_bucket_6`: Status **Enabled**

---

## Databases
*(Note: PostgreSQL RDS Instance and DB Subnet Group resources are not configured in this current infrastructure generation.)*

---

## Resource relationships
- `aws_internet_gateway.igw` is connected directly to `aws_vpc.main_vpc`.
- `aws_subnet.public-subnet` and `aws_subnet.private-subnet` reside within the IP block defined by `aws_vpc.main_vpc`.
- `aws_security_group.ecs_sg` is scoped inside `aws_vpc.main_vpc` and regulates ingress to ECS containers.
- Each `aws_s3_bucket_versioning` resource is explicitly bound to its target `aws_s3_bucket` (`uploads_bucket`, `uploads_bucket_2`, `uploads_bucket_3`, `uploads_bucket_4`, `uploads_bucket_6`).

---

# ARCHITECTURE DIAGRAM

Below is the conceptual and physical architecture diagram for the `dev` environment. It illustrates the network topology, security isolation, compute orchestration, and S3 object storage layout.

```mermaid
graph TD
    %% Internet Gateway
    IGW["🌐 Internet Gateway <br> (dev-igw)"]

    %% VPC Definition
    subgraph VPC ["VPC: dev-vpc (10.0.0.0/16)"]
        
        %% Public Subnet
        subgraph PubSubnet ["Public Subnet (10.0.1.0/24) <br> AZ: eu-west-1a"]
            PubRoute["Public Routing Table"]
        end

        %% Private Subnet
        subgraph PrivSubnet ["Private Subnet (10.0.10.0/24) <br> AZ: eu-west-1b"]
            ECS["📦 ECS Cluster: dev-cluster2 <br> (Container Tasks)"]
            SG["🔒 Security Group: dev-ecs-sg <br> (Allow TCP 3000 from VPC)"]
            
            ECS --> SG
        end
    end

    %% Storage Layer (S3 Outside VPC)
    subgraph Storage ["S3 Object Storage (eu-west-1)"]
        subgraph S3_1 ["dev-uploads"]
            B1["S3 Bucket 1"]
            V1["🔄 Versioning: Enabled"]
        end
        subgraph S3_2 ["dev-uploads-2"]
            B2["S3 Bucket 2"]
            V2["❌ Versioning: Disabled"]
        end
        subgraph S3_3 ["dev-uploads-3"]
            B3["S3 Bucket 3"]
            V3["❌ Versioning: Disabled"]
        end
        subgraph S3_4 ["dev-uploads-4"]
            B4["S3 Bucket 4"]
            V4["❌ Versioning: Disabled"]
        end
        subgraph S3_6 ["dev-uploads-6"]
            B6["S3 Bucket 6"]
            V6["🔄 Versioning: Enabled"]
        end
    end

    %% Network Connections
    IGW <--> PubRoute
    PubRoute -.-> PrivSubnet
    ECS -.-> Storage
```

### Architectural Components Description:
1. **Virtual Private Cloud (VPC):** Acts as the foundational network boundary. All networking routes and subnets are defined within this block (`10.0.0.0/16`).
2. **Public Subnet:** Positioned in Availability Zone `eu-west-1a` with a direct routing capability via the Internet Gateway (`dev-igw`) allowing inbound/outbound public internet communication.
3. **Private Subnet:** Positioned in Availability Zone `eu-west-1b`, housing compute workloads that should not be directly exposed to the open internet. 
4. **ECS Cluster (dev-cluster2):** Manages docker container tasks safely inside the Private Subnet, governed by `dev-ecs-sg` restricting traffic strictly to Port `3000` from internal network resources.
5. **S3 Storage Layer:** Contains five independent object storage buckets used for storage. Buckets `dev-uploads` and `dev-uploads-6` have version control enabled to prevent accidental deletion and preserve deployment files. Buckets `2`, `3`, and `4` have version control disabled.