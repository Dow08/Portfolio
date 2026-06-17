output "public_route_table_id" {
  description = "ID de la route table publique"
  value       = aws_route_table.public.id
}

output "private_route_table_id" {
  description = "ID de la route table privée"
  value       = aws_route_table.private.id
}