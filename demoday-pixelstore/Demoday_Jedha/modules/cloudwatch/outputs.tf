output "sns_topic_arn" {
  description = "ARN du topic SNS pour les alertes CloudWatch"
  value       = aws_sns_topic.alerts.arn
}

output "dashboard_name" {
  description = "Nom du dashboard CloudWatch"
  value       = aws_cloudwatch_dashboard.main.dashboard_name
}