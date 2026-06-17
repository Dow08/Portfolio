output "alb_dns_name" {
  description = "URL de l'application"
  value       = module.alb.alb_dns_name
}

output "vpc_id" {
  description = "ID du VPC"
  value       = module.vpc.vpc_id
}

output "public_subnet_ids" {
  description = "IDs des subnets publics"
  value       = module.subnets.public_subnet_ids
}

output "private_subnet_ids" {
  description = "IDs des subnets privés"
  value       = module.subnets.private_subnet_ids
}

output "rds_endpoint" {
  description = "Endpoint RDS"
  value       = module.rds.db_endpoint
}

output "nat_public_ip" {
  description = "IP publique du NAT Gateway"
  value       = module.nat.eip_public_ip
}

output "asg_name" {
  description = "Nom de l'Auto Scaling Group"
  value       = module.ec2_asg.asg_name
}

output "waf_arn" {
  description = "ARN du WAF"
  value       = module.waf.waf_arn
}