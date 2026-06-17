variable "vpc_cidr" {
  description = "CIDR block du VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "project_name" {
  description = "Nom du projet pour les tags"
  type        = string
  default     = "projet-02"
}

variable "env" {
  description = "Environnement"
  type        = string
  default     = "dev"
}

variable "owner" {
  description = "Propriétaire des ressources"
  type        = string
  default     = "jim"
}