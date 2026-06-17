"""
GRC Analysis — PixelStore Infrastructure AWS
Utilise les scripts de grc-agent-hermes sur les données réelles du projet.
"""
import sys, os, json, subprocess
sys.stdout.reconfigure(encoding='utf-8')

BASE  = r'C:\Users\Dow\Desktop\pixelstore\grc'
HERMES = r'C:\Users\Dow\Desktop\Cour GRC\grc-agent-hermes\grc-agent-hermes\scripts'
os.makedirs(BASE, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 1. ISO 27001:2022 — Évaluation des 93 contrôles PixelStore
# ═══════════════════════════════════════════════════════════════════════════════
ISO_DATA = """code,statut,maturite,commentaire
A.5.1,Partiel,1,Aucune politique de securite SI formalisee ni publiee
A.5.2,Partiel,2,Roles definis (RACI projet) mais non formalises dans un document officiel
A.5.3,Partiel,2,Separation partielle : SecOps/Dev/Chef de projet mais pas de politique ecrite
A.5.4,Partiel,1,Responsabilite direction non documentee — contexte academique
A.5.5,Non implemente,0,Aucun contact etabli avec autorites (ANSSI/CNIL)
A.5.6,Non implemente,0,Aucune participation a des groupes specialises cybersecurite
A.5.7,Partiel,2,Veille via Jedha Bootcamp et rapport de pentest — non systematique
A.5.8,Partiel,2,Securite integree au projet (pentest, WAF, IAM) mais sans plan formel
A.5.9,Non implemente,1,Pas d'inventaire formel des actifs — liste implicite dans Terraform
A.5.10,Non implemente,0,Aucune politique d'utilisation acceptable des actifs
A.5.11,Non implemente,0,Pas de procedure de restitution des actifs
A.5.12,Non implemente,1,Pas de classification formelle des informations
A.5.13,Non implemente,0,Pas de marquage de l'information
A.5.14,Non implemente,0,Pas de politique de transfert d'information
A.5.15,Implemente,4,IAM least privilege — SG en cascade — acces strictement controles
A.5.16,Implemente,3,IAM roles et users definis — SSM Session Manager — pas de MFA
A.5.17,Implemente,4,Secrets Manager — bcrypt passwords — aucune cle en clair
A.5.18,Implemente,3,Droits EC2 limites a S3 et Secrets Manager uniquement
A.5.19,Non implemente,0,AWS comme fournisseur — pas de clause securite formalisee
A.5.20,Non implemente,0,Pas d'accord de securite fournisseur documente
A.5.21,Non implemente,0,Chaine approvisionnement TIC non evaluee
A.5.22,Partiel,2,CloudTrail surveille les API AWS — surveillance fournisseurs non formalisee
A.5.23,Partiel,2,Architecture AWS documentee en Terraform — pas de revue securite cloud formelle
A.5.24,Non implemente,1,Pas de plan de gestion des incidents de securite
A.5.25,Non implemente,0,Pas de procedure d'evaluation et decision sur incidents
A.5.26,Non implemente,0,Pas de procedure de reponse aux incidents documentee
A.5.27,Partiel,1,Pentest realise — retour d'experience informel seulement
A.5.28,Non implemente,0,Pas de procedure de collecte et preservation des preuves
A.5.29,Partiel,2,Multi-AZ assure la continuite — pas de plan PCA formel
A.5.30,Partiel,2,Terraform permet de reconstruire l'infra — RPO/RTO definis mais non testes
A.5.31,Partiel,2,RGPD pris en compte (eu-west-3) — pas d'audit juridique complet
A.5.32,Non implemente,0,Droits propriete intellectuelle non evalues
A.5.33,Partiel,2,CloudTrail 90 jours — logs S3 — pas de politique de conservation formelle
A.5.34,Partiel,2,Donnees en France (RGPD) — pas de registre traitements — pas de DPA
A.5.35,Partiel,1,Pentest interne realise — pas de revue independante externe
A.5.36,Non implemente,0,Pas de processus de verification de conformite aux politiques
A.5.37,Partiel,2,Procedures dans Terraform et README — pas de documentation operationnelle formelle
A.6.1,Non implemente,0,Pas de verification d'antecedents (contexte academique)
A.6.2,Non implemente,0,Pas de conditions d'embauche avec clauses securite
A.6.3,Partiel,2,Formation Jedha Bootcamp — pas de programme de sensibilisation recurrent
A.6.4,Non implemente,0,Pas de processus disciplinaire
A.6.5,Non implemente,0,Pas de procedures de sortie avec securite
A.6.6,Non implemente,0,Pas d'engagements de confidentialite signes
A.6.7,Non implemente,0,Pas de politique de travail a distance
A.6.8,Non implemente,0,Pas de canal de signalement des evenements de securite
A.7.1,Implemente,4,AWS data center — securite physique geree par AWS (SOC2/ISO27001 certifie)
A.7.2,Implemente,4,Acces physiques AWS — controles par AWS
A.7.3,Implemente,4,Salles securisees — infrastructure AWS
A.7.4,Implemente,4,Surveillance physique AWS
A.7.5,Implemente,4,Protection menaces physiques — AWS
A.7.6,Implemente,4,Zones securisees — AWS
A.7.7,Non implemente,0,Politique bureau propre non applicable / non definie
A.7.8,Implemente,4,Materiel AWS — controles par AWS
A.7.9,Non implemente,0,Securite actifs hors site non definie
A.7.10,Partiel,2,S3 avec versioning et AES256 — pas de politique supports amovibles
A.7.11,Implemente,4,Services generaux — AWS
A.7.12,Implemente,4,Cablage — AWS
A.7.13,Implemente,4,Maintenance equipements — AWS
A.7.14,Implemente,4,Elimination securisee — AWS gere les disques
A.8.1,Non implemente,1,Pas de politique de gestion des terminaux utilisateurs
A.8.2,Implemente,4,IAM least privilege — aucun acces root — SSM
A.8.3,Implemente,3,SG RDS accessible uniquement depuis SG EC2 — restriction effective
A.8.4,Non implemente,1,Code source sur GitHub — pas de controle d'acces formel
A.8.5,Partiel,2,Authentification bcrypt — mais pas de MFA sur AWS ni sur l'app
A.8.6,Partiel,3,ASG adapte la capacite automatiquement selon CPU
A.8.7,Non implemente,0,Pas d'antivirus/EDR sur les instances EC2
A.8.8,Partiel,2,Pentest realise — pas de processus continu de gestion des vulnerabilites
A.8.9,Implemente,4,Toute la configuration est dans Terraform versionne sur GitHub
A.8.10,Non implemente,0,Pas de politique de suppression des donnees
A.8.11,Non implemente,0,Pas de masquage des donnees sensibles
A.8.12,Non implemente,0,Pas de DLP
A.8.13,Implemente,4,Snapshots RDS quotidiens — retention 7 jours — S3 versioning
A.8.14,Implemente,4,Architecture Multi-AZ — redondance native
A.8.15,Implemente,4,CloudTrail multi-region — logs S3 90 jours — CloudWatch
A.8.16,Implemente,4,CloudWatch 4 alarmes — GuardDuty — SNS alertes
A.8.17,Partiel,2,Synchronisation NTP AWS implicite — non explicitement configuree
A.8.18,Partiel,2,SSM Session Manager — pas de politique formelle utilitaires privileges
A.8.19,Non implemente,0,Pas de politique d'installation de logiciels
A.8.20,Implemente,4,VPC Multi-AZ — SG en cascade — NACLs — WAF
A.8.21,Implemente,4,Services reseau AWS securises — WAF sur ALB
A.8.22,Implemente,4,Subnets publics/prives separes — RDS isole
A.8.23,Non implemente,0,Pas de filtrage web sortant depuis EC2
A.8.24,Non implemente,1,Pas de TLS/HTTPS — F1 pentest critique — port 443 ferme
A.8.25,Partiel,2,Securite pensee en conception mais pas de SDLC formel
A.8.26,Partiel,2,WAF couvre OWASP — pas de revue securite formelle du code applicatif
A.8.27,Implemente,3,Architecture defense en profondeur — VPC tiers — documentee
A.8.28,Partiel,2,Requetes parametrees PyMySQL (anti-SQLi) — pas de revue code formelle
A.8.29,Partiel,2,Pentest boite grise realise — pas de SAST/DAST automatise en CI/CD
A.8.30,Non implemente,0,Pas de processus de securite pour le dev externalise
A.8.31,Non implemente,1,Pas de separation env dev/test/prod — deploiement direct en prod
A.8.32,Partiel,2,Terraform versionne sur GitHub — pas de processus de Change Management formel
A.8.33,Non implemente,0,Pas de politique de gestion des donnees de test
A.8.34,Non implemente,0,Pas de procedure de protection du SI pendant audit
"""

iso_csv = os.path.join(BASE, 'pixelstore_iso27001.csv')
with open(iso_csv, 'w', encoding='utf-8') as f:
    f.write(ISO_DATA)
print('[+] ISO 27001 CSV créé')

# ═══════════════════════════════════════════════════════════════════════════════
# 2. NIST CSF 2.0 — Scoring PixelStore
# ═══════════════════════════════════════════════════════════════════════════════
NIST_DATA = """fonction,categorie,sous_categorie,score,commentaire
GV,GV.OC,GV.OC-01,1,Mission implicitement comprise — non documentee
GV,GV.OC,GV.OC-02,1,Parties prenantes identifiees informellement (equipe 3 personnes)
GV,GV.RM,GV.RM-01,1,Politique de gestion des risques inexistante
GV,GV.RM,GV.RM-02,2,Risques identifies dans specs techniques — pas de registre formel
GV,GV.RR,GV.RR-01,2,RACI projet defini — roles securite assigns
GV,GV.PO,GV.PO-01,1,Pas de PSSI formelle
GV,GV.OV,GV.OV-01,1,Pas de gouvernance de supervision securite
GV,GV.SC,GV.SC-01,1,AWS comme fournisseur — pas d'evaluation risque fournisseur
ID,ID.AM,ID.AM-01,2,Actifs listes dans Terraform — pas d'inventaire formel
ID,ID.AM,ID.AM-02,3,Ressources cloud cataloguees via Terraform state
ID,ID.RA,ID.RA-01,2,Analyse risques dans specs techniques — EBIOS non applique
ID,ID.RA,ID.RA-02,2,Pentest identifie les vulnerabilites — pas de threat modeling formel
ID,ID.IM,ID.IM-01,1,Pas de programme d'amelioration continue identifie
PR,PR.AA,PR.AA-01,4,IAM least privilege — SSM Session Manager — bcrypt
PR,PR.AA,PR.AA-02,2,Authentification app sans MFA — AWS sans MFA
PR,PR.DS,PR.DS-01,4,AES256 RDS + S3 — Secrets Manager — chiffrement en transit VPC
PR,PR.DS,PR.DS-02,3,Requetes parametrees — WAF SQLi — SG en cascade
PR,PR.IR,PR.IR-01,1,Pas de politique de protection de l'information formelle
PR,PR.PS,PR.PS-01,4,Terraform versionne — configuration as code — immutable infra
PR,PR.PS,PR.PS-02,2,User_data script EC2 — pas de hardening OS formel (CIS Benchmark)
DE,DE.CM,DE.CM-01,4,CloudWatch alarmes — GuardDuty — CloudTrail — SNS
DE,DE.CM,DE.CM-02,3,WAF logs — ALB access logs — VPC Flow Logs
DE,DE.AE,DE.AE-01,2,Alertes SNS configurees — pas de playbook de triage
DE,DE.AE,DE.AE-02,1,Pas de correlation d'evenements (SIEM)
RS,RS.MA,RS.MA-01,1,Pas de plan de reponse aux incidents documente
RS,RS.AN,RS.AN-01,2,CloudTrail permet forensique post-incident — pas de procedure
RS,RS.CO,RS.CO-01,1,Pas de procedure de communication de crise
RS,RS.MI,RS.MI-01,2,WAF bloque en temps reel — GuardDuty alerte — pas de playbook
RC,RC.RP,RC.RP-01,2,Procedure terraform apply documentee — RPO/RTO definis mais non testes
RC,RC.BC,RC.BC-01,3,Multi-AZ assure la continuite — RDS failover auto
RC,RC.CO,RC.CO-01,1,Pas de communication post-incident definie
"""

nist_csv = os.path.join(BASE, 'pixelstore_nist_csf.csv')
with open(nist_csv, 'w', encoding='utf-8') as f:
    f.write(NIST_DATA)
print('[+] NIST CSF CSV créé')

# ═══════════════════════════════════════════════════════════════════════════════
# 3. FAIR — Scénarios de risque PixelStore
# ═══════════════════════════════════════════════════════════════════════════════
scenarios_fair = [
    {
        "nom_scenario": "Interception credentials clients (HTTP en clair — F1 pentest)",
        "description": "Absence de TLS/HTTPS : credentials utilisateurs interceptables en clair sur reseau non securise",
        "TEF": {"min": 0.5, "likely": 2.0, "max": 8.0},
        "Vuln": {"min": 0.6, "likely": 0.8, "max": 0.95},
        "PLM_par_evenement": {"min": 2000, "likely": 15000, "max": 80000},
        "SLM_par_evenement": {"min": 5000, "likely": 25000, "max": 150000}
    },
    {
        "nom_scenario": "Forge de session via SECRET_KEY faible (F8 pentest)",
        "description": "Si la SECRET_KEY Flask est triviale, un attaquant peut forger des cookies et usurper n'importe quel compte",
        "TEF": {"min": 0.1, "likely": 0.5, "max": 2.0},
        "Vuln": {"min": 0.2, "likely": 0.4, "max": 0.7},
        "PLM_par_evenement": {"min": 5000, "likely": 30000, "max": 100000},
        "SLM_par_evenement": {"min": 10000, "likely": 50000, "max": 200000}
    },
    {
        "nom_scenario": "Violation de donnees personnelles clients (RGPD — notification CNIL)",
        "description": "Fuite BDD RDS contenant emails + mots de passe : obligation notification CNIL 72h + clients",
        "TEF": {"min": 0.05, "likely": 0.2, "max": 1.0},
        "Vuln": {"min": 0.1, "likely": 0.25, "max": 0.5},
        "PLM_par_evenement": {"min": 10000, "likely": 50000, "max": 200000},
        "SLM_par_evenement": {"min": 20000, "likely": 80000, "max": 500000}
    }
]

fair_dir = os.path.join(BASE, 'fair_scenarios')
os.makedirs(fair_dir, exist_ok=True)
for sc in scenarios_fair:
    fname = sc['nom_scenario'][:40].replace(' ', '_').replace('/', '-').replace('(', '').replace(')', '') + '.json'
    path = os.path.join(fair_dir, fname)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(sc, f, ensure_ascii=False, indent=2)
print(f'[+] {len(scenarios_fair)} scénarios FAIR créés')

# ═══════════════════════════════════════════════════════════════════════════════
# 4. Exécuter les scripts
# ═══════════════════════════════════════════════════════════════════════════════

def run(script, args, label):
    cmd = ['py', '-3', os.path.join(HERMES, script)] + args
    result = subprocess.run(cmd, capture_output=True, cwd=BASE)
    try:
        result.stdout = result.stdout.decode('utf-8', errors='replace')
        result.stderr = result.stderr.decode('utf-8', errors='replace')
    except Exception:
        result.stdout = ''
        result.stderr = ''
    if result.returncode == 0:
        print(f'[+] {label} : OK')
        if result.stdout.strip():
            for line in result.stdout.strip().split('\n'):
                print(f'    {line}')
    else:
        print(f'[!] {label} ERREUR:')
        print(result.stderr[-500:] if result.stderr else '(pas de message)')
    return result.returncode == 0

print('\n=== Exécution des scripts ===')

# Gap analysis ISO 27001
run('gap_analysis_iso27001.py',
    ['--input', iso_csv, '--output', os.path.join(BASE, 'rapport_gap_iso27001.md')],
    'Gap Analysis ISO 27001')

# NIST CSF scoring
run('scoring_maturite_nist_csf.py',
    ['--input', nist_csv, '--output', os.path.join(BASE, 'rapport_nist_csf.md')],
    'Scoring NIST CSF 2.0')

# FAIR — 3 scénarios
for sc in scenarios_fair:
    fname = sc['nom_scenario'][:40].replace(' ', '_').replace('/', '-').replace('(', '').replace(')', '') + '.json'
    out_name = 'fair_' + fname.replace('.json', '.md')
    run('calcul_fair.py',
        ['--scenario', os.path.join(fair_dir, fname),
         '--output', os.path.join(BASE, out_name)],
        f'FAIR — {sc["nom_scenario"][:50]}')

print('\n=== Tous les livrables GRC générés dans:', BASE, '===')
