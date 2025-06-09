// outputs.tf
output "vpc_id" {
  description = "The ID of the VPC created"
  value       = aws_vpc.main.id
}