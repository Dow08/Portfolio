# Bucket S3 dédié au stockage des logs CloudTrail
resource "aws_s3_bucket" "cloudtrail" {
  bucket        = "${var.project_name}-${var.env}-cloudtrail-logs"
  force_destroy = true

  tags = {
    Name        = "${var.project_name}-${var.env}-cloudtrail-logs"
    Environment = var.env
    Owner       = var.owner
  }
}

# Blocage accès public - les logs ne doivent jamais être accessibles depuis internet
resource "aws_s3_bucket_public_access_block" "cloudtrail" {
  bucket = aws_s3_bucket.cloudtrail.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Chiffrement des logs au repos
resource "aws_s3_bucket_server_side_encryption_configuration" "cloudtrail" {
  bucket = aws_s3_bucket.cloudtrail.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Politique du bucket - autorise CloudTrail à écrire les logs dedans
resource "aws_s3_bucket_policy" "cloudtrail" {
  bucket = aws_s3_bucket.cloudtrail.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        # CloudTrail doit pouvoir vérifier que le bucket existe
        Sid    = "AWSCloudTrailAclCheck"
        Effect = "Allow"
        Principal = {
          Service = "cloudtrail.amazonaws.com"
        }
        Action   = "s3:GetBucketAcl"
        Resource = aws_s3_bucket.cloudtrail.arn
      },
      {
        # CloudTrail doit pouvoir écrire les fichiers de logs
        Sid    = "AWSCloudTrailWrite"
        Effect = "Allow"
        Principal = {
          Service = "cloudtrail.amazonaws.com"
        }
        Action   = "s3:PutObject"
        Resource = "${aws_s3_bucket.cloudtrail.arn}/AWSLogs/*"
        Condition = {
          StringEquals = {
            "s3:x-amz-acl" = "bucket-owner-full-control"
          }
        }
      }
    ]
  })
}

# Groupe de logs CloudWatch pour recevoir les logs CloudTrail en temps réel
resource "aws_cloudwatch_log_group" "cloudtrail" {
  name              = "/aws/cloudtrail/${var.project_name}-${var.env}"
  retention_in_days = 90

  tags = {
    Name        = "${var.project_name}-${var.env}-cloudtrail-logs"
    Environment = var.env
    Owner       = var.owner
  }
}

# Rôle IAM - autorise CloudTrail à écrire dans CloudWatch Logs
resource "aws_iam_role" "cloudtrail" {
  name = "${var.project_name}-${var.env}-cloudtrail-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "cloudtrail.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Environment = var.env
    Owner       = var.owner
  }
}

# Policy IAM - définit exactement ce que CloudTrail peut faire dans CloudWatch
resource "aws_iam_role_policy" "cloudtrail" {
  name = "${var.project_name}-${var.env}-cloudtrail-policy"
  role = aws_iam_role.cloudtrail.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "${aws_cloudwatch_log_group.cloudtrail.arn}:*"
      }
    ]
  })
}

# Le trail CloudTrail - surveille toutes les régions AWS
resource "aws_cloudtrail" "main" {
  name                          = "${var.project_name}-${var.env}-trail"
  s3_bucket_name                = aws_s3_bucket.cloudtrail.id
  include_global_service_events = true
  is_multi_region_trail         = true
  enable_log_file_validation    = true

  # Intégration CloudWatch Logs pour les alertes en temps réel
  cloud_watch_logs_group_arn = "${aws_cloudwatch_log_group.cloudtrail.arn}:*"
  cloud_watch_logs_role_arn  = aws_iam_role.cloudtrail.arn

  tags = {
    Name        = "${var.project_name}-${var.env}-trail"
    Environment = var.env
    Owner       = var.owner
  }

  depends_on = [aws_s3_bucket_policy.cloudtrail]
}