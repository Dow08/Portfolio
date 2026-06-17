# PixelStore  | Dossier Sécurité, GRC & Soutenance

> Infrastructure e-commerce sécurisée sur AWS — déploiement *Infrastructure-as-Code*, durcissement post-pentest et analyse de Gouvernance, Risques & Conformité (GRC).

Ce dépôt regroupe l'ensemble du projet PixelStore : le **code applicatif**, l'**Infrastructure-as-Code (Terraform)**, ainsi que les **livrables documentaires, sécuritaires et GRC**. Il s'agit d'une plateforme e-commerce (Flask) déployée sur AWS via Terraform, auditée par test d'intrusion puis durcie, et évaluée selon les référentiels ISO 27001, NIST CSF 2.0 et la méthode de quantification financière FAIR.

> **Sécurité :** aucun secret n'est versionné. Les fichiers sensibles (`*.tfvars`, `*.tfstate`, `.terraform/`, `.env`) sont exclus via [`.gitignore`](.gitignore). Les identifiants RDS et la `SECRET_KEY` Flask sont gérés exclusivement via AWS Secrets Manager et des variables d'environnement.

---

## 1. Contexte du projet

PixelStore est une PME e-commerce fictive (~35 salariés) servant de cas d'étude pour la conception, le déploiement et la sécurisation d'une infrastructure cloud de niveau production. Le projet couvre l'ensemble du cycle :

1. **Conception & déploiement** d'une architecture AWS multi-tiers via Terraform.
2. **Test d'intrusion** (pentest) de l'application et de l'infrastructure.
3. **Remédiation** des vulnérabilités identifiées (durcissement applicatif et réseau).
4. **Analyse GRC** : évaluation de conformité et quantification financière du risque.

---

## 2. Architecture cible

```
Client ──HTTPS──> Cloudflare ──HTTP(80)──> ALB ──HTTP(5000)──> EC2 (Gunicorn) ──> RDS MySQL
                  (TLS + WAF)              (AWS WAF)           (Auto Scaling)     (Secrets Manager)
```

| Couche | Rôle | Sécurité associée |
| :--- | :--- | :--- |
| **Cloudflare** | Terminaison TLS, CDN, WAF en bordure | Chiffrement HTTPS, *Always Use HTTPS*, HSTS |
| **ALB** | Répartition de charge | Verrouillé sur les plages IP Cloudflare (anti-contournement TLS) |
| **AWS WAF** | Pare-feu applicatif | Common Rules, anti-SQLi, *rate limiting* |
| **EC2 / Auto Scaling** | Serveurs applicatifs (Gunicorn, utilisateur non-root) | Rôle IAM au moindre privilège, accès via SSM (pas de SSH) |
| **RDS MySQL** | Base de données | Chiffrement au repos, identifiants en Secrets Manager |
| **Secrets Manager** | Gestion des secrets | Identifiants RDS + `SECRET_KEY` Flask, jamais en dur |

L'infrastructure est entièrement décrite en **Terraform modulaire** (modules : `vpc`, `subnets`, `alb`, `ec2_asg`, `rds`, `waf`, `iam`, `secrets_manager`, `cloudtrail`, `guardduty`, `cloudwatch`, `nat`, `nacl`, `security_groups`, etc.).

---

## 3. Durcissement post-pentest

Le test d'intrusion a identifié plusieurs vulnérabilités, toutes remédiées :

| ID | Constat | Correctif |
| :--- | :--- | :--- |
| **F1** | Absence de TLS (HTTP en clair) | TLS via Cloudflare + ALB verrouillé sur les IP Cloudflare |
| **F2** | Serveur de développement exposé | Passage à **Gunicorn**, `debug=False`, en-tête `Server` masqué |
| **F3** | En-têtes de sécurité absents | CSP, `X-Frame-Options`, `nosniff`, `Referrer-Policy`, **HSTS**, `Permissions-Policy` |
| **F4** | Cookies non sécurisés | `Secure` / `SameSite` / `HttpOnly` + `ProxyFix` |
| **F5** | Énumération de comptes | Messages d'inscription génériques |
| **F6 / F8** | Clé de session faible | `SECRET_KEY` forte (64 car.) générée par Terraform, stockée en Secrets Manager |
| **F7** | Pas de politique de mot de passe | Validation serveur (≥ 12 car., complexité, anti-mots-de-passe-courants) |
| **Bonus** | Open Redirect sur `/cart/add` | Redirections internes uniquement (`safe_redirect_target()`) |

---

## 4. Analyse GRC

Le volet GRC (dossier [`G.R.C/`](G.R.C/)) confronte le projet à trois référentiels :

| Référentiel | Résultat | Synthèse |
| :--- | :--- | :--- |
| **ISO/IEC 27001:2022** | 28 % de conformité effective — maturité **1,72 / 5** | Base technique solide ; écarts majoritairement administratifs (PSSI, RH, chartes) |
| **NIST CSF 2.0** | **Tier 1 — Partiel** (0,69 / 4) | Chantiers prioritaires : Réponse à incident (RS) et Reprise d'activité (RC) |
| **FAIR** (Monte-Carlo, 10 000 itérations) | Exposition ramenée de **192 000 €/an** à **17 000 €/an** | Remédiations P1 → **−175 000 €/an**, sous le seuil d'appétence (30 000 €) |

La quantification financière suit la formule FAIR `ALE = LEF × LM`, alimentée par des scénarios à trois points (méthode PERT-Beta) décrits dans [`G.R.C/fair_scenarios/`](G.R.C/fair_scenarios/).

---

## 5. Contenu du dépôt

| Fichier / Dossier | Description |
| :--- | :--- |
| [`Demoday_Jedha/`](Demoday_Jedha/) | **Code source** : application Flask (`app/`) et Infrastructure-as-Code Terraform modulaire (`modules/`, `main.tf`) |
| [`G.R.C/`](G.R.C/) | Analyse GRC complète : rapports ISO 27001 & NIST CSF, scénarios FAIR, scripts Python de génération |
| `G.R.C/run_grc.py` | Évaluation des contrôles ISO 27001 / NIST CSF et calcul FAIR |
| `G.R.C/build_rapport_pdf.py` | Génération du rapport GRC en PDF (ReportLab) |
| `G.R.C/*.csv` | Grilles d'évaluation ISO 27001 (93 contrôles) et NIST CSF |
| `G.R.C/fair_scenarios/*.json` | Paramètres des scénarios de risque (TEF, Vuln, pertes) |
| `Rapport_GRC_PixelStore_corrige.pdf` | Rapport GRC consolidé |
| `Rapport_Pentest_PixelStore_corrige.docx` | Rapport de test d'intrusion et remédiations |
| `PixelStore_Specifications_Techniques_corrige.pdf` | Spécifications techniques de l'infrastructure |
| `tech_watch_PixelStore_2026.pdf` | Veille technologique et sécurité |
| `Présentation.pptx` / `Présentation.pdf` | Support de présentation de soutenance |
| `Dorian_Speech_Soutenance_GRC_PixelStore.docx` | Script oral GRC (slides 13–16) + mémos orateur |
| `Questions_Reponses_Soutenance_PixelStore.pdf` | Préparation aux questions du jury |
| `Script_Soutenance_PixelStore.pdf` | Trame globale de soutenance |
| `TOPO MAJ 09-06.excalidraw` | Schéma d'architecture (Excalidraw) |

---

## 6. Stack technique & outils

| Domaine | Outils |
| :--- | :--- |
| **Cloud** | AWS (VPC, EC2, Auto Scaling, ALB, RDS MySQL, S3, Secrets Manager, IAM, WAF, CloudTrail, GuardDuty, CloudWatch) |
| **IaC** | Terraform `~> 1.x`, providers `hashicorp/aws ~> 5.0` & `hashicorp/random ~> 3.0`, backend S3 + verrouillage DynamoDB |
| **Application** | Python · Flask 3.1 · Gunicorn · PyMySQL · bcrypt · boto3 · cryptography |
| **Bordure / TLS** | Cloudflare (TLS *Full*, WAF, HSTS) |
| **Sécurité & GRC** | Test d'intrusion · ISO 27001:2022 · NIST CSF 2.0 · méthode FAIR (Monte-Carlo / PERT-Beta) |
| **Reporting** | Python · ReportLab · Pandoc |

---

## 7. Équipe projet

| Membre | Rôle |
| :--- | :--- |
| **Dorian Poncelet** | Responsable GRC / SecOps — développement applicatif, Terraform, gestion des secrets |
| **Jimmy Barbier** | SecOps — WAF, IAM, supervision, détection des menaces |
| **Matthieu Broquard** | Architecte Cloud & DPO — conception réseau, arbitrages de risques, FinOps |

---

## 8. Confidentialité

Plusieurs documents portent la mention **« Confidentiel — Interne »**. Aucun secret (identifiants, état Terraform, clés) n'est versionné : les fichiers sensibles (`*.tfvars`, `*.tfstate`, `.terraform/`) sont exclus via [`.gitignore`](.gitignore).
