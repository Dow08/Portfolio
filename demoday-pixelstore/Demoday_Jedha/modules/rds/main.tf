# Subnet Group RDS
resource "aws_db_subnet_group" "main" {
  name        = "${var.project_name}-db-subnet-group"
  description = "Subnet group pour RDS MySQL"
  subnet_ids  = var.private_subnet_ids

  tags = {
    Name        = "${var.project_name}-db-subnet-group"
    Environment = var.env
    Owner       = var.owner
    ManagedBy   = "Terraform"
  }
}

# Instance RDS MySQL
resource "aws_db_instance" "main" {
  identifier        = "${var.project_name}-mysql-${var.env}"
  engine            = "mysql"
  engine_version    = "8.0"
  instance_class    = var.db_instance_class
  allocated_storage = var.allocated_storage

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [var.sg_rds_id]
  parameter_group_name   = aws_db_parameter_group.main.name

  multi_az            = var.multi_az
  publicly_accessible = false
  skip_final_snapshot = true
  deletion_protection = false

  # Sauvegardes : journaux de transactions / binlogs sauvegardés en continu
  # (PITR ~15 min) tant que la rétention est > 0 ; snapshot complet planifié
  # toutes les 12 h via AWS Backup (voir backup.tf). RPO ~15 min.
  backup_retention_period = var.backup_retention_period
  backup_window           = "03:00-04:00"
  maintenance_window      = "mon:04:00-mon:05:00"

  tags = {
    Name        = "${var.project_name}-mysql"
    Environment = var.env
    Owner       = var.owner
    ManagedBy   = "Terraform"
  }
}