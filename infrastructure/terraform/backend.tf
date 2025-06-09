// backend.tf
terraform {
  required_version = ">= 1.0"
  backend "s3" {
    bucket         = "my-terraform-state-bucket"  # replace with your bucket name
    key            = "${var.project_name}/terraform.tfstate"
    region         = var.aws_region
    encrypt        = true
    dynamodb_table = "terraform-locks"            # replace with your DynamoDB table for state locking
  }
}