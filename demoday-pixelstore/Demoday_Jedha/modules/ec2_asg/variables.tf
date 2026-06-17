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
  description = "IDs des subnets publics pour les EC2"
  type        = list(string)
}

variable "sg_ec2_id" {
  description = "ID du Security Group EC2"
  type        = string
}

variable "target_group_arn" {
  description = "ARN du Target Group ALB"
  type        = string
}

variable "db_host" {
  description = "Hostname RDS"
  type        = string
}

variable "db_name" {
  description = "Nom de la base de données"
  type        = string
}

variable "db_username" {
  description = "Nom d'utilisateur RDS"
  type        = string
}

variable "db_password" {
  description = "Mot de passe RDS"
  type        = string
  sensitive   = true
}

variable "instance_type" {
  description = "Type d'instance EC2"
  type        = string
  default     = "t2.micro"
}

variable "min_size" {
  description = "Nombre minimum d'instances"
  type        = number
  default     = 1
}

variable "max_size" {
  description = "Nombre maximum d'instances"
  type        = number
  default     = 2
}

variable "desired_capacity" {
  description = "Nombre d'instances souhaité"
  type        = number
  default     = 1
}

variable "ami_id" {
  description = "ID de l'AMI Amazon Linux 2"
  type        = string
}

variable "secret_arn" {
  description = "ARN du secret Secrets Manager"
  type        = string
}

variable "instance_profile_name" {
  description = "Nom de l'instance profile IAM"
  type        = string
}

variable "s3_bucket_name" {
  description = "Nom du bucket S3 pour les images produits"
  type        = string
}