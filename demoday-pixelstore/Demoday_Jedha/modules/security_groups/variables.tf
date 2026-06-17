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

# Plages d'adresses IP de Cloudflare (https://www.cloudflare.com/ips/).
# L'ALB n'accepte le trafic QUE depuis Cloudflare : impossible de contourner
# le TLS de Cloudflare en frappant l'ALB en HTTP clair (durcissement F1).
variable "cloudflare_ip_ranges" {
  description = "Plages IPv4 de Cloudflare autorisées à joindre l'ALB"
  type        = list(string)
  default = [
    "173.245.48.0/20",
    "103.21.244.0/22",
    "103.22.200.0/22",
    "103.31.4.0/22",
    "141.101.64.0/18",
    "108.162.192.0/18",
    "190.93.240.0/20",
    "188.114.96.0/20",
    "197.234.240.0/22",
    "198.41.128.0/17",
    "162.158.0.0/15",
    "104.16.0.0/13",
    "104.24.0.0/14",
    "172.64.0.0/13",
    "131.0.72.0/22",
  ]
}