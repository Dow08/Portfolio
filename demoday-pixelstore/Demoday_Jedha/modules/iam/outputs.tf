output "instance_profile_name" {
  description = "Nom de l'instance profile IAM"
  value       = aws_iam_instance_profile.ec2_profile.name
}

output "ec2_role_arn" {
  description = "ARN du rôle IAM EC2"
  value       = aws_iam_role.ec2_role.arn
}