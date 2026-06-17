output "bucket_name" {
  description = "Nom du bucket S3 media"
  value       = aws_s3_bucket.media.id
}

output "bucket_arn" {
  description = "ARN du bucket S3 media"
  value       = aws_s3_bucket.media.arn
}