# Terraform Guide

A beginner-friendly guide to provisioning AWS infrastructure for the Fitness And Diet App using Terraform.

## Table of Contents
 1. Prerequisites
 2. Directory Structure
 3. Configuring AWS Credentials
 4. Terraform Installation
 5. Backend Configuration (Remote State)
 6. Provider Configuration
 7. Defining Variables and Outputs
 8. Sample Resource Definitions
 9. Terraform Workflow (init, plan, apply, destroy)
 10. Best Practices
 11. Further Reading

## 1. Prerequisites
 - An AWS account with permissions to create resources (VPCs, EC2, S3, RDS, IAM, etc.).
 - AWS CLI installed and configured: `aws --version`.
 - Terraform (version >= 1.0) installed: `terraform -version`.

## 2. Directory Structure
 Organize your Terraform code in its own directory, separate from application code:

 ```bash
 project-root/
 ├─ app/                        # Application source code
 ├─ docs/                       # Documentation (including this guide)
 └─ infrastructure/
    └─ terraform/
       ├─ provider.tf
       ├─ backend.tf
       ├─ variables.tf
       ├─ outputs.tf
       └─ main.tf
 ```

## 3. Configuring AWS Credentials
 Terraform uses the AWS CLI credentials by default:
 ```bash
 aws configure
 # Enter your AWS Access Key, Secret Access Key, region, and output format
 ```
 Credentials can also be set via environment variables:
 ```bash
 export AWS_ACCESS_KEY_ID="YOUR_KEY"
 export AWS_SECRET_ACCESS_KEY="YOUR_SECRET"
 export AWS_DEFAULT_REGION="us-east-1"
 ```

## 4. Terraform Installation
 Download and install Terraform from https://www.terraform.io/downloads.html. Confirm installation:
 ```bash
 terraform -version
 ```

## 5. Backend Configuration (Remote State)
 Store your Terraform state remotely in an S3 bucket for collaboration and locking with DynamoDB:
 ```hcl
 // backend.tf
 terraform {
   required_version = ">= 1.0"
   backend "s3" {
     bucket         = "my-terraform-state-bucket"
     key            = "fitness-diet-app/terraform.tfstate"
     region         = var.aws_region
     encrypt        = true
     dynamodb_table = "terraform-locks"
   }
 }
 ```
 Create the S3 bucket and DynamoDB table manually or via a separate Terraform config before using this backend.

## 6. Provider Configuration
 Define the AWS provider in `provider.tf`:
 ```hcl
 // provider.tf
 variable "aws_region" {
   description = "AWS region to deploy resources"
   type        = string
   default     = "us-east-1"
 }

 provider "aws" {
   region = var.aws_region
 }
 ```

## 7. Defining Variables and Outputs
 Declare reusable variables in `variables.tf`:
 ```hcl
 // variables.tf
 variable "environment" {
   description = "Deployment environment (e.g., dev, staging, prod)"
   type        = string
   default     = "dev"
 }

 variable "project_name" {
   description = "Project name"
   type        = string
   default     = "fitness-diet-app"
 }
 ```
 Expose important data with outputs in `outputs.tf`:
 ```hcl
 // outputs.tf
 output "vpc_id" {
   description = "The ID of the VPC created"
   value       = aws_vpc.main.id
 }
 ```

## 8. Sample Resource Definitions
 Below is a simple example in `main.tf` to create a VPC and public subnet:
 ```hcl
 // main.tf
 resource "aws_vpc" "main" {
   cidr_block = "10.0.0.0/16"
   tags = {
     Name = "${var.project_name}-${var.environment}-vpc"
   }
 }

 resource "aws_subnet" "public" {
   vpc_id                  = aws_vpc.main.id
   cidr_block              = "10.0.1.0/24"
   map_public_ip_on_launch = true
   tags = {
     Name = "${var.project_name}-${var.environment}-public-subnet"
   }
 }
 ```
 Extend this file with additional AWS services as needed: RDS for PostgreSQL, ECS/Fargate, S3 buckets, IAM roles, etc.

## 9. Terraform Workflow
 1. **Initialize**:
    ```bash
    cd infrastructure/terraform
    terraform init
    ```
 2. **Validate** (optional):
    ```bash
    terraform validate
    ```
 3. **Plan**:
    ```bash
    terraform plan -var="environment=dev" -out=plan.out
    ```
 4. **Apply**:
    ```bash
    terraform apply "plan.out"
    ```
 5. **Destroy** (when you need to tear down):
    ```bash
    terraform destroy -var="environment=dev"
    ```

## 10. Best Practices
 - Use a remote backend (S3 + DynamoDB) for state storage and locking.
 - Do not check Terraform state files (`.tfstate`) into version control.
 - Organize code into modules for reusable components.
 - Leverage Terraform workspaces for managing multiple environments.
 - Tag AWS resources with `environment`, `project`, `owner` for cost tracking.

## 11. Further Reading
 - Official Terraform Documentation: https://www.terraform.io/docs
 - AWS Provider Docs: https://registry.terraform.io/providers/hashicorp/aws/latest/docs
 - Terraform AWS Modules: https://github.com/terraform-aws-modules
 - AWS Architecture Guide: see [AWS_Achitecure.md](AWS_Achitecure.md) for high-level patterns.