// provider.tf
variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

provider "aws" {
  region = var.aws_region
}