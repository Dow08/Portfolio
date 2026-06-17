# ---------------------------------------------------------------------------
# Sauvegardes RDS : binlogs/PITR (~15 min) + snapshot complet toutes les 12 h
# ---------------------------------------------------------------------------

# Parameter group : binlog au format ROW (sauvegarde fine / PITR / réplication)
resource "aws_db_parameter_group" "main" {
  name_prefix = "${var.project_name}-mysql-"
  family      = "mysql8.0"
  description = "Binlog ROW pour PITR / sauvegarde des journaux"

  parameter {
    name  = "binlog_format"
    value = "ROW"
  }

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name        = "${var.project_name}-mysql-params"
    Environment = var.env
    Owner       = var.owner
  }
}

# Coffre AWS Backup dédié aux snapshots RDS
resource "aws_backup_vault" "rds" {
  name = "${var.project_name}-rds-backup-vault-${var.env}"

  tags = {
    Name        = "${var.project_name}-rds-backup-vault"
    Environment = var.env
    Owner       = var.owner
  }
}

# Rôle IAM utilisé par AWS Backup
resource "aws_iam_role" "backup" {
  name = "${var.project_name}-rds-backup-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "backup.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "backup" {
  role       = aws_iam_role.backup.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForBackup"
}

# Plan de sauvegarde : un snapshot complet toutes les 12 h, conservé 7 jours
resource "aws_backup_plan" "rds" {
  name = "${var.project_name}-rds-12h"

  rule {
    rule_name         = "snapshot-12h"
    target_vault_name = aws_backup_vault.rds.name
    schedule          = "cron(0 0/12 * * ? *)" # 00:00 et 12:00 UTC
    start_window      = 60
    completion_window = 180

    lifecycle {
      delete_after = 7
    }
  }

  tags = {
    Name        = "${var.project_name}-rds-12h"
    Environment = var.env
    Owner       = var.owner
  }
}

# Sélection : applique le plan à l'instance RDS
resource "aws_backup_selection" "rds" {
  name         = "${var.project_name}-rds-selection"
  iam_role_arn = aws_iam_role.backup.arn
  plan_id      = aws_backup_plan.rds.id
  resources    = [aws_db_instance.main.arn]
}
