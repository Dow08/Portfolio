output "sg_alb_id" {
  description = "ID du Security Group ALB"
  value       = aws_security_group.alb.id
}

output "sg_ec2_id" {
  description = "ID du Security Group EC2"
  value       = aws_security_group.ec2.id
}

output "sg_rds_id" {
  description = "ID du Security Group RDS"
  value       = aws_security_group.rds.id
}