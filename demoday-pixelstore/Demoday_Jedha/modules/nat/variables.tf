variable "public_subnet_id" {
  description = "ID du subnet public AZ-a pour le NAT Gateway"
  type        = string
}

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