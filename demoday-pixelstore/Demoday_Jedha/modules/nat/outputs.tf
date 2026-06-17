output "nat_gateway_id" {
  description = "ID du NAT Gateway"
  value       = aws_nat_gateway.main.id
}

output "eip_public_ip" {
  description = "Adresse IP publique de l'Elastic IP"
  value       = aws_eip.nat.public_ip
}