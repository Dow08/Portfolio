# Détecteur GuardDuty - le service de détection des menaces
resource "aws_guardduty_detector" "main" {
  enable = true

  datasources {
    s3_logs {
      enable = true
    }
    kubernetes {
      audit_logs {
        enable = false
      }
    }
    malware_protection {
      scan_ec2_instance_with_findings {
        ebs_volumes {
          enable = true
        }
      }
    }
  }

  tags = {
    Name        = "${var.project_name}-${var.env}-guardduty"
    Environment = var.env
    Owner       = var.owner
  }
}

# Règle EventBridge - intercepte les findings GuardDuty de sévérité MEDIUM et HIGH
resource "aws_cloudwatch_event_rule" "guardduty_findings" {
  name        = "${var.project_name}-${var.env}-guardduty-findings"
  description = "Capture les findings GuardDuty de sévérité moyenne et haute"

  event_pattern = jsonencode({
    source      = ["aws.guardduty"]
    detail-type = ["GuardDuty Finding"]
    detail = {
      severity = [
        { numeric = [">=", 4] }
      ]
    }
  })

  tags = {
    Name        = "${var.project_name}-${var.env}-guardduty-findings"
    Environment = var.env
    Owner       = var.owner
  }
}

# Cible EventBridge - envoie les findings vers SNS pour alerter par email
resource "aws_cloudwatch_event_target" "guardduty_sns" {
  rule      = aws_cloudwatch_event_rule.guardduty_findings.name
  target_id = "GuardDutyToSNS"
  arn       = var.sns_topic_arn

  input_transformer {
    input_paths = {
      severity    = "$.detail.severity"
      type        = "$.detail.type"
      description = "$.detail.description"
      region      = "$.region"
      time        = "$.time"
    }
    input_template = "\"ALERTE SECURITE PixelStore - Finding GuardDuty\\nSévérité: <severity>\\nType: <type>\\nDescription: <description>\\nRégion: <region>\\nHeure: <time>\""
  }
}

# Permission - autorise EventBridge à publier sur le topic SNS
resource "aws_sns_topic_policy" "guardduty" {
  arn = var.sns_topic_arn

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowEventBridgeToPublish"
        Effect = "Allow"
        Principal = {
          Service = "events.amazonaws.com"
        }
        Action   = "sns:Publish"
        Resource = var.sns_topic_arn
      }
    ]
  })
}