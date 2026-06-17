output "guardduty_detector_id" {
  description = "ID du détecteur GuardDuty"
  value       = aws_guardduty_detector.main.id
}

output "guardduty_detector_arn" {
  description = "ARN du détecteur GuardDuty"
  value       = aws_guardduty_detector.main.arn
}