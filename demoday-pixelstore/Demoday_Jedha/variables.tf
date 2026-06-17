variable "aws_region" {
  description = "Région AWS"
  type        = string
  default     = "eu-west-3"
}

variable "project_name" {
  description = "Nom du projet"
  type        = string
  default     = "pixelstore"
}

variable "env" {
  description = "Environnement"
  type        = string
  default     = "prod"
}

variable "owner" {
  description = "Propriétaire des ressources"
  type        = string
  default     = "jim"
}

variable "vpc_cidr" {
  description = "CIDR block du VPC"
  type        = string
  default     = "10.0.0.0/16"
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
  description = "Zones de disponibilité"
  type        = list(string)
  default     = ["eu-west-3a", "eu-west-3b"]
}

variable "db_username" {
  description = "Nom d'utilisateur RDS"
  type        = string
  default     = "admin"
}

variable "db_password" {
  description = "Mot de passe RDS"
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "Nom de la base de données"
  type        = string
  default     = "pixelstore_db"
}

variable "instance_type" {
  description = "Type d'instance EC2"
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "ID AMI Amazon Linux 2 eu-west-3"
  type        = string
  default     = "ami-0f61de2873e29e866"
}

variable "db_instance_class" {
  description = "Type d'instance RDS"
  type        = string
  default     = "db.t3.micro"
}

variable "multi_az" {
  description = "Activer le Multi-AZ RDS"
  type        = bool
  default     = true
}

variable "backup_retention_period" {
  description = "Rétention des sauvegardes RDS en jours (>0 active PITR / binlogs ~15 min)"
  type        = number
  default     = 7
}

variable "alarm_email" {
  description = "Adresse email pour recevoir les alertes CloudWatch"
  type        = string
}