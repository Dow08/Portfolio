# PixelStore - E-commerce sécurisé sur AWS

Application e-commerce (Flask) déployée sur AWS via Terraform, durcie à la suite
d'un test d'intrusion (rapport PixelStore, 8 juin 2026) et placée derrière
**Cloudflare** pour le chiffrement TLS.

## Architecture

```
Client -HTTPS--> Cloudflare (TLS) -HTTP(80)--> ALB -HTTP(5000)--> EC2 (Gunicorn) --> RDS MySQL
                       (WAF CF)                  (AWS WAF)          (ASG)             (Secrets Manager)
```

- **TLS** : terminé par Cloudflare (hors code, voir plus bas).
- **WAF AWS** : Common Rules + SQLi + Rate limiting (jugés efficaces au pentest).
- **Secrets** : identifiants RDS **et** `SECRET_KEY` Flask dans AWS Secrets Manager.
- **App** : servie par Gunicorn (serveur WSGI de production), sous utilisateur non-root.

## Correctifs apportés suite au pentest

| ID | Constat | Correction |
|----|---------|------------|
| **F1** | Pas de TLS (HTTP clair) | TLS via Cloudflare + **ALB verrouillé sur les IP Cloudflare** (`modules/security_groups`) : impossible de contourner le TLS en frappant l'ALB en clair |
| **F2** | Serveur de dev Werkzeug | **Gunicorn** + `debug=False` + en-tête `Server` masqué |
| **F3** | En-têtes de sécurité absents | `after_request` : CSP, `X-Frame-Options: DENY`, `nosniff`, `Referrer-Policy`, **HSTS**, `Permissions-Policy` |
| **F4** | Cookie sans SameSite/Secure | `SESSION_COOKIE_SECURE/SAMESITE/HTTPONLY` + `ProxyFix` (schéma https reconstruit derrière CF/ALB) |
| **F5** | Énumération de comptes | Message d'inscription générique |
| **F6/F8** | Identité côté client / SECRET_KEY | `SECRET_KEY` forte (64 car., `random_password`) générée par Terraform, stockée dans Secrets Manager, **jamais en dur** ; l'app refuse de démarrer sans clé |
| **F7** | Pas de politique MDP | Validation serveur : >= 12 car., minuscule/majuscule/chiffre/spécial, anti-mots-de-passe-courants |
| **Hors pentest** | **Open Redirect** sur `/cart/add` (`next`) | `safe_redirect_target()` : redirections internes uniquement + robustesse des entrées `product_id`/`qty` |

Durcissement complémentaire : service Flask exécuté sous l'utilisateur système
non privilégié `appuser` (au lieu de root).

## Intégration Cloudflare (TLS - réalisée hors code)

1. Ajouter le domaine dans Cloudflare et déléguer les NS chez le registrar.
2. Créer un **CNAME** (proxied / nuage orange) vers le DNS public de l'ALB
   (`terraform output alb_dns_name`).
3. SSL/TLS -> mode **Full** (idéalement *Full (strict)* avec certificat d'origine
   sur l'ALB ; sinon *Flexible* : CF->ALB en HTTP port 80).
4. Activer **Always Use HTTPS** et **HSTS** côté Cloudflare.
5. Les plages IP Cloudflare autorisées sur l'ALB sont dans
   `modules/security_groups/variables.tf` (`cloudflare_ip_ranges`). À
   resynchroniser depuis <https://www.cloudflare.com/ips/> si besoin.

> Le verrouillage de l'ALB sur les IP Cloudflare est **essentiel** : sans lui,
> un attaquant peut joindre l'ALB directement en HTTP et contourner le TLS.

## Déploiement

Prérequis fournis hors dépôt (non versionnés) :

- `terraform.tfvars` (valeurs du projet ; ne contient pas le mot de passe).
  Un modèle est fourni : copier `terraform.tfvars.example` en `terraform.tfvars`
  et l'adapter.
- Le mot de passe RDS, passé en variable d'environnement (jamais commité).
- Des credentials AWS valides sur le compte cible.

```bash
cp terraform.tfvars.example terraform.tfvars   # puis adapter (alarm_email, etc.)
export TF_VAR_db_password="<mot_de_passe_RDS_fort>"

terraform init
terraform apply
```

`app.zip` et les images produits sont publiés sur S3 **automatiquement** par
Terraform (`modules/s3`, ressources `aws_s3_object`), puis récupérés par les EC2
au démarrage. Aucun upload manuel n'est nécessaire.

### Backend Terraform (état distant)

`main.tf` utilise un backend S3 partagé par l'équipe :

```hcl
backend "s3" {
  bucket         = "projet-02-terraform-state"
  dynamodb_table = "projet-02-terraform-locks"
  region         = "eu-west-3"
}
```

- **Compte AWS de l'équipe** : le bucket et la table existent déjà, rien à faire.
- **Déploiement sur un autre compte AWS** : ce bucket/table n'existe pas. Avant
  `terraform init`, deux options :
  1. créer un bucket S3 + une table DynamoDB (clé primaire `LockID`) dans le
     compte cible, puis adapter les noms dans le bloc `backend "s3"` ;
  2. ou commenter le bloc `backend "s3"` pour utiliser un **état local**
     (`terraform.tfstate` sur le disque - suffisant pour un déploiement isolé).

## Développement local

Créer un fichier `.env` (ignoré par git) :

```
SECRET_KEY=<clé_de_dev_forte>
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=password
DB_NAME=pixelstore_db
```

```bash
pip install -r app/requirements.txt
python app/app.py   # 127.0.0.1:5000, debug désactivé
```
