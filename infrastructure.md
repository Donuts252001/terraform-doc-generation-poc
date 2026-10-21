# AWS Infrastructure Documentation

- **Infrastructure overview:** Development environment provisioning via Terraform incorporating VPC, Subnets, Internet Gateway, Security Groups, RDS PostgreSQL database, ECS cluster, and S3 storage buckets with versioning configurations.
- **Documentation by:** Terraform
- **Updated date:** 2026-10-21 07:26:15 UTC
- **Commit ID:** 3d66b85
- **Environment:** dev
- **AWS region:** `eu-west-1`

---

## VPC and Networking

### Resource: AWS VPC
- **Resource type:** `aws_vpc`
- **Resource name:** `main_vpc` (`dev-vpc`)
- **Location:** AWS Region `eu-west-1`
- **Purpose:** Primary Virtual Private Cloud for network isolation of the development environment.
- **Important settings:**
  - CIDR Block: `10.0.0.0/16`
  - DNS Hostnames: Enabled (`true`)
  - DNS Support: Enabled (`true`)
  - Instance Tenancy: `default`
  - Tags: `Environment = dev`, `ManagedBy = Terraform`, `Name = dev-vpc`
- **Dependencies/relationships/connections:** Parent resource for subnets, internet gateway, and security groups.
- **Desired and current capacity/instances:** 1 VPC.

---

## Subnets

### Resource: AWS Subnet (Public)
- **Resource type:** `aws_subnet`
- **Resource name:** `public-subnet` (`dev-public-subnet`)
- **Location:** `eu-west-1a`
- **Purpose:** Public-facing subnet for resources requiring direct internet access.
- **Important settings:**
  - CIDR Block: `10.0.1.0/24`
  - Map Public IP on Launch: Enabled (`true`)
  - Tags: `Name = dev-public-subnet`, `Type = Public`
- **Dependencies/relationships/connections:** Associated with `aws_vpc.main_vpc`.
- **Desired and current capacity/instances:** 1 subnet instance.

### Resource: AWS Subnet (Private)
- **Resource type:** `aws_subnet`
- **Resource name:** `private-subnet` (`dev-private-subnet`)
- **Location:** `eu-west-1b`
- **Purpose:** Private subnet for internal-only resources like backend services and databases.
- **Important settings:**
  - CIDR Block: `10.0.10.0/24`
  - Map Public IP on Launch: Disabled (`false`)
  - Tags: `Name = dev-private-subnet`, `Type = Private`
- **Dependencies/relationships/connections:** Associated with `aws_vpc.main_vpc`.
- **Desired and current capacity/instances:** 1 subnet instance.

---

## Internet/NAT Gateways

### Resource: AWS Internet Gateway
- **Resource type:** `aws_internet_gateway`
- **Resource name:** `igw` (`dev-igw`)
- **Location:** AWS Region `eu-west-1`
- **Purpose:** Enables access to the internet for instances within public subnets.
- **Important settings:**
  - Tags: `Name = dev-igw`
- **Dependencies/relationships/connections:** Connected to `aws_vpc.main_vpc`.
- **Desired and current capacity/instances:** 1 Internet Gateway.

---

## Security Groups

### Resource: AWS Security Group (ECS)
- **Resource type:** `aws_security_group`
- **Resource name:** `ecs_sg` (`dev-ecs-sg`)
- **Location:** AWS Region `eu-west-1`
- **Purpose:** Controls network traffic to ECS container instances.
- **Important settings:**
  - Ingress: Port `3000` (TCP) from CIDR `10.0.0.0/16`.
  - Egress: All ports (`-1`) to `0.0.0.0/0`.
  - Tags: `Name = dev-ecs-sg`
- **Dependencies/relationships/connections:** Associated with `aws_vpc.main_vpc`.
- **Desired and current capacity/instances:** 1 Security Group.

### Resource: AWS Security Group (RDS)
- **Resource type:** `aws_security_group`
- **Resource name:** `rds_sg` (`dev-rds-sg`)
- **Location:** AWS Region `eu-west-1`
- **Purpose:** Controls network traffic to the RDS PostgreSQL database instance.
- **Important settings:**
  - Ingress: Port `5432` (TCP) 
  - Tags: `Name = dev-rds-sg`
- **Dependencies/relationships/connections:** Associated with `aws_vpc.main_vpc`.
- **Desired and current capacity/instances:** 1 Security Group.

---

## Compute Resources

### Resource: AWS ECS Cluster
- **Resource type:** `aws_ecs_cluster`
- **Resource name:** `main_ecs2` (`dev-cluster2`)
- **Location:** AWS Region `eu-west-1`
- **Purpose:** Container orchestration cluster for running microservices.
- **Important settings:**
  - Container Insights: Enabled (`enabled`)
  - Tags: `Environment = dev`, `ManagedBy = Terraform`
- **Dependencies/relationships/connections:** Standalone ECS cluster resource.
- **Desired and current capacity/instances:** 1 ECS Cluster.

---

## Storage Resources

### Resource: AWS S3 Buckets and Versioning
- **Resource types:** `aws_s3_bucket`, `aws_s3_bucket_versioning`
- **Location:** AWS Region `eu-west-1`
- **Purpose:** Object storage buckets configured for environment uploads and assets.
- **Important settings:**
  - **Bucket 1:** 
    - Name Prefix: `dev-uploads-bucket-`
    - Tags: `Name = dev-uploads`, `Environment = dev`, `ManagedBy = Terraform`
    - Versioning Status: Enabled
  - **Bucket 2:** 
    - Name Prefix: `dev-uploads-bucket-2`
    - Tags: `Name = dev-uploads-2`, `Environment = dev`, `ManagedBy = Terraform`
    - Versioning Status: Disabled
  - **Bucket 3:** 
    - Name Prefix: `dev-uploads-bucket-3`
    - Tags: `Name = dev-uploads-3`, `Environment = dev`, `ManagedBy = Terraform`
    - Versioning Status: Disabled
  - **Bucket 4:** 
    - Name Prefix: `dev-uploads-bucket-4`
    - Tags: `Name = dev-uploads-4`, `Environment = dev`, `ManagedBy = Terraform`
    - Versioning Status: Disabled
- **Dependencies/relationships/connections:** Independent S3 buckets with dedicated versioning configurations.
- **Desired and current capacity/instances:** 4 S3 buckets.

---

## Databases

### Resource: AWS DB Subnet Group
- **Resource type:** `aws_db_subnet_group`
- **Resource name:** `main_db_subnet_grp` (`dev-db-subnet-group`)
- **Location:** AWS Region `eu-west-1`
- **Purpose:** Encapsulates subnets for RDS deployment.
- **Important settings:**
  - Description: Managed by Terraform
  - Tags: `Name = dev-db-subnet-group`
- **Dependencies/relationships/connections:** Links to VPC subnets.

### Resource: AWS RDS Database Instance
- **Resource type:** `aws_db_instance`
- **Resource name:** `postgres` (`dev-postgres`)
- **Location:** AWS Region `eu-west-1`
- **Purpose:** Managed relational database instance for application data storage.
- **Important settings:**
  - Engine: `postgres` (Version `16`)
  - Instance Class: `db.t3.micro`
  - Allocated Storage: `20` GB
  - Master Username: `postgres`
  - DB Subnet Group: `dev-db-subnet-group`
  - Parameter Group: `default.postgres16`
  - Publicly Accessible: `false`
  - Skip Final Snapshot: `true` (automated deletion safeguard)
  - Tags: `Environment = dev`, `ManagedBy = Terraform`, `Name = dev-postgres`
- **Dependencies/relationships/connections:** Depends on `aws_db_subnet_group.main_db_subnet_grp` and `aws_security_group.rds_sg`.
- **Desired and current capacity/instances:** 1 RDS instance.

---

## Load Balancers
*(No changes or operations logged for load balancers)*

---

## Monitoring and Logging
- **ECS Cluster Insights:** Container Insights enabled on `aws_ecs_cluster.main_ecs2`.

---

## Resource Relationships
- **VPC (`aws_vpc.main_vpc`)** contains:
  - Public Subnet (`aws_subnet.public-subnet`) connected to Internet Gateway (`aws_internet_gateway.igw`).
  - Private Subnet (`aws_subnet.private-subnet`) containing DB Subnet Group (`aws_db_subnet_group.main_db_subnet_grp`).
- **RDS Instance (`aws_db_instance.postgres`)** is associated with:
  - DB Subnet Group (`aws_db_subnet_group.main_db_subnet_grp`)
  - Security Group (`aws_security_group.rds_sg`)
- **ECS Security Group (`aws_security_group.ecs_sg`)** allows traffic within the `10.0.0.0/16` VPC CIDR block on port `3000`.

---

## Important Configuration Details
- All infrastructure resources are tagged uniformly with `Environment = dev` and `ManagedBy = Terraform` where applicable.
- Passwords and sensitive outputs (such as RDS master password) are managed securely through Terraform state and encrypted parameters.