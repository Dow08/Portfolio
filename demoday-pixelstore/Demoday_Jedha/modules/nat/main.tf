resource "aws_eip" "nat" {
  domain = "vpc"

  tags = {
    Name        = "${var.project_name}-eip-nat"
    Environment = var.env
    Owner       = var.owner
    ManagedBy   = "Terraform"
  }
}

resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = var.public_subnet_id

  tags = {
    Name        = "${var.project_name}-nat"
    Environment = var.env
    Owner       = var.owner
    ManagedBy   = "Terraform"
  }

  depends_on = [aws_eip.nat]
}