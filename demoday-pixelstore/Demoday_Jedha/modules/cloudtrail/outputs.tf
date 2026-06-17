output "cloudtrail_arn" {
  description = "ARN du trail CloudTrail"
  value       = aws_cloudtrail.main.arn
}

output "cloudtrail_bucket_name" {
  description = "Nom du bucket S3 des logs CloudTrail"
  value       = aws_s3_bucket.cloudtrail.id
}

output "cloudtrail_log_group_name" {
  description = "Nom du groupe de logs CloudWatch"
  value       = aws_cloudwatch_log_group.cloudtrail.name
}