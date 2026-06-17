variable "project_name" {
  description = "Nom du projet pour les tags"
  type        = string
}

variable "env" {
  description = "Environnement"
  type        = string
}

variable "owner" {
  description = "Propriétaire des ressources"
  type        = string
}

variable "secret_arn" {
  description = "ARN du secret Secrets Manager"
  type        = string
}

variable "s3_bucket_arn" {
  description = "ARN du bucket S3 media pour la policy least privilege"
  type        = string
}