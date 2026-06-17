resource "aws_internet_gateway" "main" {
  vpc_id = var.vpc_id

  tags = {
    Name        = "${var.project_name}-igw"
    Environment = var.env
    Owner       = var.owner
    ManagedBy   = "Terraform"
  }
}