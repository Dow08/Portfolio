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

variable "public_subnet_cidrs" {
  description = "CIDRs des subnets publics"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDRs des subnets privés"
  type        = list(string)
  default     = ["10.0.3.0/24", "10.0.4.0/24"]
}

variable "availability_zones" {
  description = "Liste des AZ à utiliser"
  type        = list(string)
  default     = ["eu-west-3a", "eu-west-3b"]
}