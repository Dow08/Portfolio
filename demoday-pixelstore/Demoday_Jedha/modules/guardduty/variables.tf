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

variable "sns_topic_arn" {
  description = "ARN du topic SNS pour envoyer les alertes GuardDuty"
  type        = string
}