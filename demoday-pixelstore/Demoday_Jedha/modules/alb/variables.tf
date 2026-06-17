variable "vpc_id" {
  description = "ID du VPC"
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

variable "public_subnet_ids" {
  description = "IDs des subnets publics pour l'ALB"
  type        = list(string)
}

variable "sg_alb_id" {
  description = "ID du Security Group ALB"
  type        = string
}