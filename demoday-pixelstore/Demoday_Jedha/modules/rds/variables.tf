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

variable "private_subnet_ids" {
  description = "IDs des subnets privés pour RDS"
  type        = list(string)
}

variable "sg_rds_id" {
  description = "ID du Security Group RDS"
  type        = string
}

variable "db_username" {
  description = "Nom d'utilisateur de la base de données"
  type        = string
}

variable "db_password" {
  description = "Mot de passe de la base de données"
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "Nom de la base de données"
  type        = string
}

variable "db_instance_class" {
  description = "Type d'instance RDS"
  type        = string
  default     = "db.t3.micro"
}

variable "allocated_storage" {
  description = "Stockage alloué en GB"
  type        = number
  default     = 20
}

variable "multi_az" {
  description = "Activer le Multi-AZ"
  type        = bool
  default     = true
}

variable "backup_retention_period" {
  description = "Rétention des sauvegardes automatiques RDS en jours (>0 active le PITR / binlogs)"
  type        = number
  default     = 7
}