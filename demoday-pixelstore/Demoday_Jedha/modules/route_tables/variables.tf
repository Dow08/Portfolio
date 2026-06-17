variable "vpc_id" {
  description = "ID du VPC"
  type        = string
}

variable "igw_id" {
  description = "ID de l'Internet Gateway"
  type        = string
}

variable "nat_gateway_id" {
  description = "ID du NAT Gateway"
  type        = string
}

variable "public_subnet_ids" {
  description = "IDs des subnets publics"
  type        = list(string)
}

variable "private_subnet_ids" {
  description = "IDs des subnets privés"
  type        = list(string)
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