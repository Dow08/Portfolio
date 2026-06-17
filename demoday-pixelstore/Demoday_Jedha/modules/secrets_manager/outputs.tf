output "secret_arn" {
  description = "ARN du secret Secrets Manager"
  value       = aws_secretsmanager_secret.db_credentials.arn
}

output "secret_name" {
  description = "Nom du secret Secrets Manager"
  value       = aws_secretsmanager_secret.db_credentials.name
}

output "db_username" {
  description = "Nom d'utilisateur de la base de données"
  value       = var.db_username
}

output "db_name" {
  description = "Nom de la base de données"
  value       = var.db_name
}

output "db_password" {
  description = "Mot de passe de la base de données"
  value       = var.db_password
  sensitive   = true
}