output "alb_dns_name" {
  description = "DNS de l'ALB pour accéder à l'application"
  value       = aws_lb.main.dns_name
}

output "alb_arn" {
  description = "ARN de l'ALB"
  value       = aws_lb.main.arn
}

output "target_group_arn" {
  description = "ARN du Target Group"
  value       = aws_lb_target_group.main.arn
}

output "alb_zone_id" {
  description = "Zone ID de l'ALB"
  value       = aws_lb.main.zone_id
}

output "alb_arn_suffix" {
  description = "Suffixe ARN de l'ALB pour les métriques CloudWatch"
  value       = aws_lb.main.arn_suffix
}

output "target_group_arn_suffix" {
  description = "Suffixe ARN du Target Group pour les métriques CloudWatch"
  value       = aws_lb_target_group.main.arn_suffix
}