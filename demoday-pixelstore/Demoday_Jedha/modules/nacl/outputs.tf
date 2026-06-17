output "nacl_public_id" {
  description = "ID de la NACL publique"
  value       = aws_network_acl.public.id
}

output "nacl_private_id" {
  description = "ID de la NACL privée"
  value       = aws_network_acl.private.id
}