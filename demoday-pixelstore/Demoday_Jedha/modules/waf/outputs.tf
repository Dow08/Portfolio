output "waf_arn" {
  description = "ARN du WAF Web ACL"
  value       = aws_wafv2_web_acl.main.arn
}

output "waf_id" {
  description = "ID du WAF Web ACL"
  value       = aws_wafv2_web_acl.main.id
}