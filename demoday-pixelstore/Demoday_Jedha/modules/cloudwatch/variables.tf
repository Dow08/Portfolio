variable "project_name" {
  description = "Nom du projet"
  type        = string
}

variable "env" {
  description = "Environnement (dev, prod...)"
  type        = string
}

variable "owner" {
  description = "Propriétaire du projet"
  type        = string
}

variable "asg_name" {
  description = "Nom de l'Auto Scaling Group à surveiller"
  type        = string
}

variable "alb_arn_suffix" {
  description = "Suffixe ARN de l'ALB pour les métriques CloudWatch"
  type        = string
}

variable "target_group_arn_suffix" {
  description = "Suffixe ARN du Target Group pour les métriques CloudWatch"
  type        = string
}

variable "db_instance_identifier" {
  description = "Identifiant de l'instance RDS à surveiller"
  type        = string
}

variable "alarm_email" {
  description = "Adresse email pour recevoir les alertes CloudWatch"
  type        = string
}