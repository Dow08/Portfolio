#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère le rapport GRC PixelStore en PDF avec reportlab.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import BalancedColumns
from reportlab.lib.colors import HexColor
from datetime import date

OUTPUT = r"C:\Users\Dow\Desktop\pixelstore\grc\Rapport_GRC_PixelStore.pdf"

# ── Palette ───────────────────────────────────────────────────────────────────
DARK        = HexColor("#0D1B2A")
GOLD        = HexColor("#C9A04B")
LIGHT_GOLD  = HexColor("#F0D9A8")
GREY_BG     = HexColor("#F4F5F7")
GREY_LINE   = HexColor("#DEE2E6")
RED         = HexColor("#C0392B")
ORANGE      = HexColor("#E67E22")
GREEN       = HexColor("#27AE60")
BLUE        = HexColor("#2980B9")
WHITE       = colors.white
BLACK       = colors.black

# ── Styles ────────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

COVER_TITLE   = S("CoverTitle",   fontSize=28, leading=34, textColor=WHITE,       fontName="Helvetica-Bold",  alignment=TA_LEFT)
COVER_SUB     = S("CoverSub",     fontSize=13, leading=18, textColor=LIGHT_GOLD,  fontName="Helvetica",       alignment=TA_LEFT)
COVER_META    = S("CoverMeta",    fontSize=9,  leading=13, textColor=LIGHT_GOLD,  fontName="Helvetica",       alignment=TA_LEFT)

H1            = S("H1",           fontSize=15, leading=20, textColor=WHITE,       fontName="Helvetica-Bold",  spaceBefore=0,  spaceAfter=6,  backColor=DARK, leftIndent=-0.5*cm, rightIndent=-0.5*cm, borderPad=8)
H2            = S("H2",           fontSize=11, leading=15, textColor=DARK,        fontName="Helvetica-Bold",  spaceBefore=10, spaceAfter=4,  borderPad=0)
H3            = S("H3",           fontSize=9.5,leading=13, textColor=GOLD,        fontName="Helvetica-Bold",  spaceBefore=6,  spaceAfter=2)

BODY          = S("Body",         fontSize=8.5,leading=12, textColor=HexColor("#2C3E50"), fontName="Helvetica", spaceAfter=4, alignment=TA_JUSTIFY)
BODY_BOLD     = S("BodyBold",     fontSize=8.5,leading=12, textColor=HexColor("#2C3E50"), fontName="Helvetica-Bold", spaceAfter=4)
SMALL         = S("Small",        fontSize=7.5,leading=11, textColor=HexColor("#555"),    fontName="Helvetica", spaceAfter=2)
CAPTION       = S("Caption",      fontSize=7,  leading=10, textColor=HexColor("#777"),    fontName="Helvetica-Oblique", alignment=TA_CENTER, spaceAfter=4)

BULLET        = S("Bullet",       fontSize=8.5,leading=12, textColor=HexColor("#2C3E50"), fontName="Helvetica",
                  leftIndent=14, firstLineIndent=-10, spaceAfter=2)

NOTE          = S("Note",         fontSize=7.5,leading=11, textColor=HexColor("#444"),    fontName="Helvetica-Oblique",
                  backColor=HexColor("#FEFCE8"), leftIndent=8, rightIndent=8, borderPad=4, spaceAfter=6)

VERDICT_RED   = S("VerdictRed",   fontSize=10, leading=14, textColor=WHITE,       fontName="Helvetica-Bold",
                  backColor=RED,   borderPad=6, alignment=TA_CENTER, spaceAfter=6)
VERDICT_AMBER = S("VerdictAmber", fontSize=10, leading=14, textColor=WHITE,       fontName="Helvetica-Bold",
                  backColor=ORANGE,borderPad=6, alignment=TA_CENTER, spaceAfter=6)
VERDICT_GREEN = S("VerdictGreen", fontSize=10, leading=14, textColor=WHITE,       fontName="Helvetica-Bold",
                  backColor=GREEN, borderPad=6, alignment=TA_CENTER, spaceAfter=6)

TOC_ENTRY     = S("TocEntry",     fontSize=9,  leading=14, textColor=DARK,        fontName="Helvetica", spaceAfter=2)

# ── Table style helpers ───────────────────────────────────────────────────────
def table_style_header():
    return TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), DARK),
        ("TEXTCOLOR",    (0,0), (-1,0), GOLD),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,0), 7.5),
        ("BOTTOMPADDING",(0,0), (-1,0), 5),
        ("TOPPADDING",   (0,0), (-1,0), 5),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[GREY_BG, WHITE]),
        ("FONTNAME",     (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE",     (0,1), (-1,-1), 7.5),
        ("TOPPADDING",   (0,1), (-1,-1), 3),
        ("BOTTOMPADDING",(0,1), (-1,-1), 3),
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("GRID",         (0,0), (-1,-1), 0.3, GREY_LINE),
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
    ])

def score_color(score, max_s):
    ratio = score / max_s if max_s else 0
    if ratio >= 0.6:   return HexColor("#D5F5E3")
    if ratio >= 0.35:  return HexColor("#FDEBD0")
    return HexColor("#FADBD8")

def b(text): return f"<b>{text}</b>"
def i(text): return f"<i>{text}</i>"
def p(text, style=None): return Paragraph(text, style or BODY)
def sp(h=0.2): return Spacer(1, h*cm)
def hr(): return HRFlowable(width="100%", thickness=0.5, color=GREY_LINE, spaceAfter=4)

# ── Page template ─────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    w, h = A4
    if doc.page == 1:
        return
    canvas.saveState()
    # Header bar
    canvas.setFillColor(DARK)
    canvas.rect(0, h - 1.1*cm, w, 1.1*cm, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.setFont("Helvetica-Bold", 7)
    canvas.drawString(1.5*cm, h - 0.7*cm, "RAPPORT GRC — PIXELSTORE")
    canvas.setFillColor(LIGHT_GOLD)
    canvas.setFont("Helvetica", 7)
    canvas.drawRightString(w - 1.5*cm, h - 0.7*cm, f"CONFIDENTIEL — {date.today().strftime('%d/%m/%Y')}")
    # Footer
    canvas.setFillColor(GREY_LINE)
    canvas.rect(0, 0, w, 0.8*cm, fill=1, stroke=0)
    canvas.setFillColor(HexColor("#555"))
    canvas.setFont("Helvetica", 6.5)
    canvas.drawString(1.5*cm, 0.28*cm, "Jedha Bootcamp — Cybersécurité Fullstack — Projet PixelStore")
    canvas.drawRightString(w - 1.5*cm, 0.28*cm, f"Page {doc.page}")
    canvas.restoreState()

# ── Cover page ────────────────────────────────────────────────────────────────
def cover():
    w, h = A4
    story = []

    # Full dark background drawn via canvas — simulate with a large table
    cover_table = Table([[""]], colWidths=[w], rowHeights=[h])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK),
    ]))

    # Gold accent line
    gold_bar = Table([[""]], colWidths=[w], rowHeights=[0.4*cm])
    gold_bar.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), GOLD)]))

    elems = []
    elems.append(Spacer(1, 3.5*cm))
    elems.append(Paragraph("RAPPORT GRC", COVER_TITLE))
    elems.append(Spacer(1, 0.2*cm))
    elems.append(Paragraph("Gouvernance · Risques · Conformité", COVER_SUB))
    elems.append(Spacer(1, 0.4*cm))
    elems.append(Paragraph("Projet PixelStore — Infrastructure AWS sécurisée", COVER_SUB))
    elems.append(Spacer(1, 1.5*cm))
    sep = Table([[""]], colWidths=[5*cm], rowHeights=[0.25*cm])
    sep.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),GOLD)]))
    elems.append(sep)
    elems.append(Spacer(1, 1.5*cm))
    meta_style = S("MetaL", fontSize=8, leading=13, textColor=LIGHT_GOLD, fontName="Helvetica")
    for line in [
        f"Date : {date.today().strftime('%d %B %Y')}",
        "Auteurs : Matthieu Broquard · Dorian Poncelet · Jimmy Barbier",
        "Formation : Jedha Bootcamp — Cybersécurité Fullstack",
        "Classification : CONFIDENTIEL",
        "Référentiels : ISO 27001:2022 · NIST CSF 2.0 · FAIR · RGPD",
    ]:
        elems.append(Paragraph(line, meta_style))

    return elems, cover_table

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=1.5*cm, rightMargin=1.5*cm,
        topMargin=1.6*cm, bottomMargin=1.4*cm,
        title="Rapport GRC PixelStore",
        author="Matthieu Broquard, Dorian Poncelet, Jimmy Barbier",
        subject="ISO 27001 / NIST CSF / FAIR — PixelStore AWS",
    )

    story = []

    # ─── COVER ────────────────────────────────────────────────────────────────
    elems, bg = cover()
    # Draw cover via a frame overlay — use a dark-background Table as underlay
    story.append(bg)
    # Actually we can't layer — use a single wide table with all content
    story = []
    # Rebuild cover as one dark Table
    cover_rows = []
    cover_rows.append([Spacer(1, 3*cm)])
    cover_rows.append([Paragraph("RAPPORT GRC", COVER_TITLE)])
    cover_rows.append([Paragraph("Gouvernance · Risques · Conformité", COVER_SUB)])
    cover_rows.append([Spacer(1, 0.2*cm)])
    cover_rows.append([Paragraph("Projet PixelStore — Infrastructure AWS sécurisée", COVER_SUB)])
    cover_rows.append([Spacer(1, 1.2*cm)])
    sep_inner = Table([[""]], colWidths=[5*cm], rowHeights=[0.2*cm])
    sep_inner.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),GOLD)]))
    cover_rows.append([sep_inner])
    cover_rows.append([Spacer(1, 1.2*cm)])
    meta_style = S("MetaL2", fontSize=8.5, leading=14, textColor=LIGHT_GOLD, fontName="Helvetica")
    for line in [
        f"Date : {date.today().strftime('%d %B %Y')}",
        "Auteurs : Matthieu Broquard · Dorian Poncelet · Jimmy Barbier",
        "Formation : Jedha Bootcamp — Cybersécurité Fullstack",
        "Classification : CONFIDENTIEL",
        "Référentiels : ISO 27001:2022 · NIST CSF 2.0 · FAIR · RGPD",
    ]:
        cover_rows.append([Paragraph(line, meta_style)])
    cover_rows.append([Spacer(1, 4*cm)])
    footer_style = S("FooterStyle", fontSize=7.5, leading=11, textColor=HexColor("#8899AA"), fontName="Helvetica-Oblique")
    cover_rows.append([Paragraph("Analyse réalisée avec GRC Agent Hermes — scripts ISO 27001, NIST CSF 2.0, FAIR Monte Carlo", footer_style)])

    w_content = A4[0] - 3*cm
    cover_t = Table([[row[0]] for row in cover_rows], colWidths=[w_content])
    cover_t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), DARK),
        ("LEFTPADDING",   (0,0), (-1,-1), 0.8*cm),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0.8*cm),
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
    ]))
    story.append(cover_t)
    story.append(PageBreak())

    # ─── SOMMAIRE ─────────────────────────────────────────────────────────────
    story.append(p(b("SOMMAIRE"), H1))
    story.append(sp(0.3))
    toc_items = [
        ("1.", "Présentation du projet PixelStore", "3"),
        ("2.", "Méthodologie d'analyse", "3"),
        ("3.", "Gap Analysis ISO 27001:2022 — résultats", "4"),
        ("4.", "Scoring maturité NIST CSF 2.0 — résultats", "6"),
        ("5.", "Quantification FAIR — exposition financière", "7"),
        ("6.", "Plan de traitement des risques prioritaires", "9"),
        ("7.", "Synthèse et recommandations", "10"),
    ]
    toc_data = [[Paragraph(n, SMALL), Paragraph(t, TOC_ENTRY), Paragraph(pg, SMALL)] for n,t,pg in toc_items]
    toc_table = Table(toc_data, colWidths=[0.7*cm, 13.3*cm, 1*cm])
    toc_table.setStyle(TableStyle([
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[GREY_BG, WHITE]),
        ("TOPPADDING",   (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("LEFTPADDING",  (0,0),(-1,-1), 6),
        ("RIGHTPADDING", (0,0),(-1,-1), 6),
        ("ALIGN",        (2,0),(-1,-1), "RIGHT"),
        ("LINEBELOW",    (0,-1),(-1,-1), 0.5, GREY_LINE),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # ─── 1. PRÉSENTATION DU PROJET ────────────────────────────────────────────
    story.append(p("1. PRÉSENTATION DU PROJET PIXELSTORE", H1))
    story.append(sp(0.2))

    story.append(p(b("Contexte"), H2))
    story.append(p(
        "PixelStore est une application e-commerce de vente de smartphones développée dans le cadre "
        "du cursus Jedha Bootcamp Cybersécurité Fullstack. Le projet couvre le développement "
        "applicatif (Flask 3.1, Python), le déploiement sur infrastructure AWS via Terraform IaC, "
        "et la sécurisation de l'ensemble de la chaîne.", BODY))

    infra_data = [
        [b("Composant"), b("Détail"), b("Statut sécurité")],
        ["Application",   "Flask 3.1 — 9 smartphones (799€–1 899€)",       "HTTP uniquement (pas de TLS)"],
        ["Compute",       "EC2 Auto Scaling Group — t2.micro min1/max2",    "SSM Session Manager (sans clé SSH)"],
        ["Load Balancer", "Application Load Balancer — Multi-AZ eu-west-3", "WAF attaché (OWASP + SQLi + RateLimit)"],
        ["Base de données","RDS MySQL — Multi-AZ — db.t3.micro",            "Chiffré au repos — subnet privé"],
        ["Stockage",      "S3 — assets statiques",                          "Chiffré SSE-S3"],
        ["Secrets",       "AWS Secrets Manager",                            "Rotation configurable"],
        ["Observabilité", "CloudWatch (4 alarmes) + GuardDuty + CloudTrail","Actif — alertes CPU/erreurs"],
        ["IaC",           "Terraform — 17 modules — 71 ressources",         "1 terraform apply (~15 min)"],
        ["RPO / RTO",     "RPO 24h (snapshots RDS daily)",                  "RTO 15 min (terraform apply)"],
    ]
    infra_t = Table(infra_data, colWidths=[3.5*cm, 7*cm, 4.5*cm])
    infra_t.setStyle(table_style_header())
    story.append(infra_t)
    story.append(sp(0.3))

    story.append(p(b("Périmètre du présent rapport"), H2))
    story.append(p(
        "L'analyse GRC porte sur l'intégralité du périmètre technique et organisationnel du projet : "
        "application Flask, infrastructure AWS, pratiques de développement et gestion de projet. "
        "Elle se base exclusivement sur les éléments observés — code source, configuration Terraform, "
        "rapport de pentest interne et documentation disponible.", BODY))
    story.append(PageBreak())

    # ─── 2. MÉTHODOLOGIE ──────────────────────────────────────────────────────
    story.append(p("2. MÉTHODOLOGIE D'ANALYSE", H1))
    story.append(sp(0.2))

    story.append(p(
        "L'analyse a été conduite en trois phases indépendantes, correspondant à trois référentiels complémentaires. "
        "Chaque phase produit un résultat quantifié et des écarts actionnables.", BODY))

    meth_data = [
        [b("Phase"), b("Référentiel"), b("Outil utilisé"), b("Résultat produit")],
        ["1 — Conformité",   "ISO 27001:2022",  "gap_analysis_iso27001.py",     "Score maturité CMMI par contrôle"],
        ["2 — Maturité",     "NIST CSF 2.0",    "scoring_maturite_nist_csf.py", "Score par fonction (0–4) + Tier"],
        ["3 — Financier",    "FAIR Monte Carlo", "calcul_fair.py",               "ALE annuel en euros (P50/P90/P95)"],
    ]
    meth_t = Table(meth_data, colWidths=[3*cm, 3.5*cm, 5*cm, 3.5*cm])
    meth_t.setStyle(table_style_header())
    story.append(meth_t)
    story.append(sp(0.3))

    story.append(p(b("Échelles de mesure"), H2))
    scales_data = [
        [b("Référentiel"), b("Échelle"), b("Seuil de conformité visé")],
        ["ISO 27001:2022", "CMMI 0 → 5 (0=inexistant, 5=optimisé)", "Maturité ≥ 3 sur 90% des contrôles applicables"],
        ["NIST CSF 2.0",   "Tier 1 → 4 (1=Partial, 4=Adaptive)",     "Tier 3 (Repeatable) — objectif organisations matures"],
        ["FAIR",           "ALE en € — percentiles P50/P90/P95",      "P90 utilisé comme référence budget de défense"],
    ]
    scales_t = Table(scales_data, colWidths=[3.5*cm, 6*cm, 5.5*cm])
    scales_t.setStyle(table_style_header())
    story.append(scales_t)
    story.append(sp(0.3))

    story.append(p(b("Sources d'information"), H2))
    for src in [
        "Code source Flask (app.py, models.py, routes.py)",
        "Infrastructure Terraform (17 modules — main.tf, variables.tf, outputs.tf par module)",
        "Rapport de pentest interne — 8 findings documentés (F1 à F8)",
        "Configuration AWS (WAF rules, Security Groups, NACLs, IAM policies, CloudWatch alarms)",
        "Documentation projet (README, notes d'architecture)",
    ]:
        story.append(p(f"• {src}", BULLET))
    story.append(PageBreak())

    # ─── 3. ISO 27001 ─────────────────────────────────────────────────────────
    story.append(p("3. GAP ANALYSIS ISO 27001:2022", H1))
    story.append(sp(0.2))

    story.append(p(b("Résultats globaux"), H2))

    kpi_data = [
        [b("Indicateur"), b("Valeur")],
        ["Contrôles évalués",                "93 / 93 (couverture 100%)"],
        ["Contrôles conformes (maturité ≥ 3)", "26 / 93 — 28%"],
        ["Score moyen de maturité",           "1,72 / 5"],
        ["Verdict",                           "Programme de mise en conformité 12–18 mois"],
    ]
    kpi_t = Table(kpi_data, colWidths=[7*cm, 8*cm])
    kpi_t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), DARK),
        ("TEXTCOLOR",    (0,0), (-1,0), GOLD),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 8.5),
        ("TOPPADDING",   (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("BACKGROUND",   (0,-1), (-1,-1), HexColor("#FADBD8")),
        ("FONTNAME",     (0,1), (-1,-1), "Helvetica"),
        ("GRID",         (0,0), (-1,-1), 0.3, GREY_LINE),
    ]))
    story.append(kpi_t)
    story.append(sp(0.3))

    story.append(p(b("Score par thème ISO 27001"), H2))
    themes_data = [
        [b("Thème"), b("Contrôles"), b("Score moyen"), b("Conformes ≥ 3"), b("Niveau")],
        ["A.7 — Physiques",       "14", "3,29 / 5", "11 / 14 (79%)", "Satisfaisant"],
        ["A.8 — Technologiques",  "34", "1,97 / 5", "11 / 34 (32%)", "Insuffisant"],
        ["A.5 — Organisationnels","37", "1,22 / 5", " 4 / 37 (11%)", "Critique"],
        ["A.6 — Personnels",      " 8", "0,25 / 5", " 0 /  8 (0%)",  "Critique"],
    ]
    themes_t = Table(themes_data, colWidths=[5.5*cm, 2*cm, 2.5*cm, 3.5*cm, 2.5*cm])
    ts = table_style_header()
    ts.add("BACKGROUND", (0,1), (-1,1), HexColor("#D5F5E3"))
    ts.add("BACKGROUND", (0,2), (-1,2), HexColor("#FDEBD0"))
    ts.add("BACKGROUND", (0,3), (-1,3), HexColor("#FADBD8"))
    ts.add("BACKGROUND", (0,4), (-1,4), HexColor("#FADBD8"))
    story.append(Table(themes_data, colWidths=[5.5*cm, 2*cm, 2.5*cm, 3.5*cm, 2.5*cm], style=ts))
    story.append(sp(0.2))
    story.append(p(
        i("Note : Le score A.7 (Physiques) est élevé car AWS gère la sécurité physique des datacenters "
          "(datacenter locks, CCTV, accès biométrique) — ces contrôles sont délégués par contrat."), NOTE))

    story.append(p(b("Écarts majeurs par thème"), H2))
    story.append(p(b("A.5 — Contrôles organisationnels (score 1,22/5)"), H3))
    gaps_a5 = [
        [b("Contrôle"), b("Intitulé"), b("Maturité"), b("Observation")],
        ["A.5.5",  "Contact avec les autorités",         "0", "Aucun contact établi avec ANSSI / CNIL"],
        ["A.5.19", "Sécurité fournisseurs",               "0", "AWS comme fournisseur — aucune clause sécurité formalisée"],
        ["A.5.25", "Évaluation incidents",                "0", "Pas de procédure d'évaluation et décision sur incidents"],
        ["A.5.26", "Réponse aux incidents",               "0", "Pas de procédure de réponse documentée"],
        ["A.5.28", "Collecte des preuves",                "0", "Pas de procédure de préservation des preuves"],
        ["A.5.36", "Conformité avec politiques",          "0", "Pas de processus de vérification de conformité aux politiques"],
    ]
    story.append(Table(gaps_a5, colWidths=[1.8*cm, 4.5*cm, 1.8*cm, 7*cm],
                       style=table_style_header()))
    story.append(sp(0.2))

    story.append(p(b("A.6 — Contrôles personnels (score 0,25/5) — Thème le plus critique"), H3))
    gaps_a6 = [
        [b("Contrôle"), b("Intitulé"), b("Maturité"), b("Observation")],
        ["A.6.1", "Vérification des antécédents",    "0", "Absence totale — contexte académique sans processus RH"],
        ["A.6.2", "Conditions d'embauche sécurité",  "0", "Pas de clauses sécurité dans les engagements"],
        ["A.6.5", "Responsabilités après emploi",    "0", "Pas de procédure de départ sécurisé"],
        ["A.6.6", "Engagements de confidentialité",  "0", "Aucun NDA / engagement signé"],
        ["A.6.7", "Politique travail à distance",    "0", "Pas de politique formalisée"],
        ["A.6.8", "Signalement événements sécurité", "0", "Aucun canal de signalement défini"],
    ]
    story.append(Table(gaps_a6, colWidths=[1.8*cm, 4.5*cm, 1.8*cm, 7*cm],
                       style=table_style_header()))
    story.append(sp(0.2))

    story.append(p(b("A.8 — Contrôles technologiques (score 1,97/5) — Écarts liés au pentest"), H3))
    gaps_a8 = [
        [b("Contrôle"), b("Intitulé"), b("Maturité"), b("Lien pentest"), b("Observation")],
        ["A.8.24", "Utilisation de la cryptographie", "0", "F1 — HTTPS absent",       "HTTP en clair — credentials exposés"],
        ["A.8.11", "Masquage de données",              "0", "F5 — Énumération users",  "Pas de masquage champs sensibles"],
        ["A.8.12", "Prévention fuites (DLP)",          "0", "—",                       "Aucun outil DLP configuré"],
        ["A.8.31", "Séparation dev/test/prod",         "0", "F8 — SECRET_KEY",         "Même clé utilisée en dev et prod"],
        ["A.8.33", "Données de test",                  "0", "—",                       "Pas de politique données de test"],
    ]
    story.append(Table(gaps_a8, colWidths=[1.8*cm, 3.5*cm, 1.8*cm, 3*cm, 5*cm],
                       style=table_style_header()))
    story.append(PageBreak())

    # ─── 4. NIST CSF ──────────────────────────────────────────────────────────
    story.append(p("4. SCORING MATURITÉ NIST CSF 2.0", H1))
    story.append(sp(0.2))

    story.append(p(b("Résultats globaux"), H2))

    nist_kpi = [
        [b("Indicateur"), b("Valeur")],
        ["Sous-catégories évaluées", "77 / 77"],
        ["Score moyen global",       "0,69 / 4"],
        ["Niveau global",            "Tier 1 — Partial (ad hoc, réactif)"],
        ["Objectif cible",           "Tier 3 — Repeatable (formalisé, mesuré)"],
    ]
    kpi_t2 = Table(nist_kpi, colWidths=[7*cm, 8*cm])
    kpi_t2.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), DARK),
        ("TEXTCOLOR",    (0,0), (-1,0), GOLD),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 8.5),
        ("TOPPADDING",   (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("FONTNAME",     (0,1), (-1,-1), "Helvetica"),
        ("GRID",         (0,0), (-1,-1), 0.3, GREY_LINE),
    ]))
    story.append(kpi_t2)
    story.append(sp(0.3))

    story.append(p(b("Score par fonction NIST CSF 2.0"), H2))
    nist_data = [
        [b("Fonction"), b("Description"), b("Score"), b("Tier"), b("Priorité")],
        ["PR — Protect",  "Contrôles de protection",           "1,18 / 4", "Tier 1", "Bonne base (IAM, chiffrement, réseau)"],
        ["ID — Identify",  "Connaissance actifs et risques",   "0,83 / 4", "Tier 1", "Cartographie des flux manquante"],
        ["DE — Detect",    "Détection événements et anomalies","0,73 / 4", "Tier 1", "Corrélation événements absente"],
        ["GV — Govern",    "Stratégie de gestion du risque",   "0,62 / 4", "Tier 1", "Aucune politique formalisée"],
        ["RC — Recover",   "Reprise après incident",           "0,25 / 4", "—",      "CRITIQUE — aucun plan de reprise"],
        ["RS — Respond",   "Réponse aux incidents",            "0,23 / 4", "—",      "CRITIQUE — aucune procédure"],
    ]
    nist_t = Table(nist_data, colWidths=[3*cm, 4*cm, 2*cm, 1.8*cm, 4.7*cm])
    nts = table_style_header()
    nts.add("BACKGROUND", (0,1), (-1,1), HexColor("#D5F5E3"))
    nts.add("BACKGROUND", (0,2), (-1,2), HexColor("#EBF5FB"))
    nts.add("BACKGROUND", (0,3), (-1,3), HexColor("#EBF5FB"))
    nts.add("BACKGROUND", (0,4), (-1,4), HexColor("#FDEBD0"))
    nts.add("BACKGROUND", (0,5), (-1,5), HexColor("#FADBD8"))
    nts.add("BACKGROUND", (0,6), (-1,6), HexColor("#FADBD8"))
    story.append(Table(nist_data, colWidths=[3*cm, 4*cm, 2*cm, 1.8*cm, 4.7*cm], style=nts))
    story.append(sp(0.2))

    story.append(p(b("Visualisation — Niveaux de maturité par fonction (sur 4)"), H3))
    radar_data = [
        ("GV — Govern",   0.62), ("ID — Identify", 0.83), ("PR — Protect",  1.18),
        ("DE — Detect",   0.73), ("RS — Respond",  0.23), ("RC — Recover",  0.25),
    ]
    bar_rows = [
        [b("Fonction"), b("Niveau de maturité"), b("Score")]
    ]
    for fn, score in radar_data:
        filled = int(round((score / 4.0) * 25))
        empty  = 25 - filled
        bar_str = "█" * filled + "░" * empty
        bar_color_hex = "#27AE60" if score >= 1.5 else ("#E67E22" if score >= 0.7 else "#C0392B")
        bar_rows.append([
            fn,
            Paragraph(f'<font color="{bar_color_hex}">{bar_str}</font>', S("BarP", fontSize=8, fontName="Helvetica")),
            f"{score:.2f} / 4"
        ])
    bar_container = Table(bar_rows, colWidths=[3.5*cm, 9*cm, 2.5*cm])
    bar_container.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), DARK),
        ("TEXTCOLOR",     (0,0), (-1,0), GOLD),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 8),
        ("TOPPADDING",    (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING",   (0,0), (-1,-1), 5),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [GREY_BG, WHITE]),
        ("GRID",          (0,0), (-1,-1), 0.3, GREY_LINE),
    ]))
    story.append(bar_container)
    story.append(sp(0.3))

    story.append(p(b("Écarts critiques — Fonctions RS et RC (61 écarts total)"), H2))
    story.append(p(
        "Les fonctions RS (Respond) et RC (Recover) sont quasi inexistantes. "
        "Les 13 sous-catégories RS et 8 sous-catégories RC sont toutes à score 0.", BODY))
    rs_rc_data = [
        [b("Code"), b("Sous-catégorie"), b("Fonction"), b("Score"), b("Action requise")],
        ["RS.MA-01", "Plan de réponse exécuté",            "Respond", "0", "Créer un plan de réponse aux incidents"],
        ["RS.MA-02", "Incidents triés et validés",          "Respond", "0", "Définir critères de triage"],
        ["RS.AN-07", "Preuves préservées",                  "Respond", "0", "Procédure forensique minimale"],
        ["RS.AN-08", "Cause racine déterminée",             "Respond", "0", "Post-mortem structuré"],
        ["RS.CO-02", "Parties prenantes notifiées",         "Respond", "0", "Plan de communication incident"],
        ["RC.RP-01", "Plan de reprise exécuté",             "Recover", "0", "Tester le terraform apply comme PRA"],
        ["RC.RP-03", "Intégrité sauvegardes vérifiée",     "Recover", "0", "Tester les snapshots RDS"],
        ["RC.RP-04", "Fonctions critiques restaurées",      "Recover", "0", "Documenter l'ordre de restauration"],
    ]
    story.append(Table(rs_rc_data, colWidths=[2.2*cm, 4.3*cm, 2*cm, 1.5*cm, 5*cm],
                       style=table_style_header()))
    story.append(PageBreak())

    # ─── 5. FAIR ──────────────────────────────────────────────────────────────
    story.append(p("5. QUANTIFICATION FAIR — EXPOSITION FINANCIÈRE", H1))
    story.append(sp(0.2))
    story.append(p(
        "Trois scénarios de risque ont été quantifiés via simulation Monte Carlo (10 000 itérations). "
        "Chaque scénario est modélisé selon le modèle FAIR : ALE = LEF × LM, avec LEF = TEF × Vuln "
        "et LM = PLM + SLM. Les hypothèses sont issues du rapport de pentest et de l'analyse de l'infrastructure.", BODY))

    story.append(p(b("Synthèse des trois scénarios"), H2))
    fair_summary = [
        [b("Scénario"), b("Source"), b("ALE moyen /an"), b("P90 /an"), b("P95 /an")],
        ["F1 — HTTP en clair\n(interception credentials)",
         "Pentest F1\nAbsence HTTPS",
         "144 800 €", "275 000 €", "331 600 €"],
        ["F8 — SECRET_KEY faible\n(forge de session Flask)",
         "Pentest F8\nClé triviale",
         " 30 200 €", " 57 200 €", " 70 700 €"],
        ["RGPD — Fuite BDD RDS\n(notification CNIL 72h)",
         "Analyse infra\nRDS exposable",
         " 17 000 €", " 33 700 €", " 43 200 €"],
        [b("TOTAL exposition annuelle"), "", b("~192 000 €"), b("~366 000 €"), b("~446 000 €")],
    ]
    fst = table_style_header()
    fst.add("BACKGROUND", (0,4), (-1,4), HexColor("#2C3E50"))
    fst.add("TEXTCOLOR",  (0,4), (-1,4), GOLD)
    fst.add("FONTNAME",   (0,4), (-1,4), "Helvetica-Bold")
    story.append(Table(fair_summary, colWidths=[5*cm, 3*cm, 2.8*cm, 2.5*cm, 2.7*cm],
                       style=fst))
    story.append(sp(0.3))

    story.append(p(
        i("Lecture : P90 = dans 90% des simulations, la perte annuelle sera inférieure à cette valeur. "
          "La valeur P90 est la référence recommandée pour dimensionner le budget de défense."), NOTE))
    story.append(sp(0.2))

    # Scenario 1
    story.append(p(b("Scénario 1 — Interception de credentials (HTTP en clair — F1 pentest)"), H2))
    s1_hyp = [
        [b("Facteur FAIR"), b("Min"), b("Mode (likely)"), b("Max"), b("Description")],
        ["TEF (fréquence tentatives/an)", "0,5",   "2,0",    "8,0",    "Attaque de type MITM sur réseau non sécurisé"],
        ["Vuln (probabilité de succès)",  "0,60",  "0,80",   "0,95",   "Absence de TLS — interception triviale"],
        ["PLM (perte directe /événement)","2 k€",  "15 k€",  "80 k€",  "Remédiation technique + notification clients"],
        ["SLM (perte secondaire /évén.)", "5 k€",  "25 k€",  "150 k€", "Atteinte réputation + sanctions potentielles"],
    ]
    story.append(Table(s1_hyp, colWidths=[4.5*cm, 1.5*cm, 2*cm, 1.5*cm, 5.5*cm],
                       style=table_style_header()))
    s1_res = [
        [b("Statistique"), b("ALE"), b("LEF (événements/an)"), b("LM (perte/événement)")],
        ["Moyenne (P50)",   "144 800 €",  "2,17",  "66 400 €"],
        ["P75",             "192 600 €",  "—",     "—"],
        ["P90 — référence", "275 000 €",  "3,64",  "104 500 €"],
        ["P95",             "331 600 €",  "—",     "—"],
        ["P99",             "448 200 €",  "—",     "—"],
    ]
    rts = table_style_header()
    rts.add("BACKGROUND", (0,4), (-1,4), HexColor("#FADBD8"))
    story.append(sp(0.15))
    story.append(Table(s1_res, colWidths=[3.5*cm, 3*cm, 4*cm, 4.5*cm], style=rts))
    story.append(sp(0.15))
    story.append(p(
        "Un certificat TLS via AWS Certificate Manager (ACM) est gratuit. "
        "L'activation sur l'ALB représente moins de 2h de travail et élimine "
        "l'intégralité de ce scénario — soit ~145 k€/an d'exposition supprimée.", BODY))

    story.append(sp(0.2))

    # Scenario 2
    story.append(p(b("Scénario 2 — Forge de session via SECRET_KEY faible (F8 pentest)"), H2))
    s2_hyp = [
        [b("Facteur FAIR"), b("Min"), b("Mode"), b("Max"), b("Description")],
        ["TEF", "0,1",  "0,5", "2,0",  "Attaquant ciblé découvrant la clé par bruteforce ou exposition"],
        ["Vuln","0,20", "0,40","0,70", "Clé triviale — forge de cookie de session réalisable"],
        ["PLM", "5 k€", "30 k€","100 k€","Usurpation comptes + remédiation"],
        ["SLM", "10 k€","50 k€","200 k€","Atteinte réputation + notification RGPD possible"],
    ]
    story.append(Table(s2_hyp, colWidths=[1.5*cm, 1.5*cm, 2*cm, 1.5*cm, 8.5*cm],
                       style=table_style_header()))
    s2_res = [
        [b("Statistique"), b("ALE"), b("P90"), b("P95")],
        ["Moyenne", "30 200 €", "57 200 €", "70 700 €"],
    ]
    story.append(sp(0.1))
    story.append(Table(s2_res, colWidths=[3.5*cm, 3.5*cm, 3.5*cm, 4.5*cm],
                       style=table_style_header()))
    story.append(sp(0.15))
    story.append(p(
        "Correction : générer une SECRET_KEY de 32 octets aléatoires via secrets.token_hex(32) "
        "et la stocker dans AWS Secrets Manager. Durée : 30 minutes.", BODY))

    story.append(sp(0.2))

    # Scenario 3
    story.append(p(b("Scénario 3 — Violation de données personnelles clients (RGPD — notification CNIL)"), H2))
    s3_hyp = [
        [b("Facteur FAIR"), b("Min"), b("Mode"), b("Max"), b("Description")],
        ["TEF", "0,05","0,20","1,00", "Fuite BDD RDS via exploitation combinée des vulnérabilités"],
        ["Vuln","0,10","0,25","0,50", "Mitigé par subnet privé RDS et Security Groups"],
        ["PLM", "10 k€","50 k€","200 k€","Investigation + notification CNIL (72h) + clients"],
        ["SLM", "20 k€","80 k€","500 k€","Amende RGPD possible + perte de confiance"],
    ]
    story.append(Table(s3_hyp, colWidths=[1.5*cm, 1.5*cm, 2*cm, 1.5*cm, 8.5*cm],
                       style=table_style_header()))
    s3_res = [
        [b("Statistique"), b("ALE"), b("P90"), b("P95")],
        ["Moyenne", "17 000 €", "33 700 €", "43 200 €"],
    ]
    story.append(sp(0.1))
    story.append(Table(s3_res, colWidths=[3.5*cm, 3.5*cm, 3.5*cm, 4.5*cm],
                       style=table_style_header()))
    story.append(sp(0.15))
    story.append(p(
        "Ce risque est partiellement mitigé par l'architecture (RDS en subnet privé, Security Groups restrictifs). "
        "L'ajout de TLS (scénario 1) réduit également ce scénario en limitant l'exposition des credentials "
        "qui pourraient servir de vecteur d'entrée.", BODY))
    story.append(PageBreak())

    # ─── 6. PLAN DE TRAITEMENT ────────────────────────────────────────────────
    story.append(p("6. PLAN DE TRAITEMENT DES RISQUES PRIORITAIRES", H1))
    story.append(sp(0.2))
    story.append(p(
        "Les actions sont classées par priorité selon deux critères : impact sur l'exposition financière FAIR "
        "et facilité de mise en œuvre. Les actions de niveau P1 peuvent être réalisées en moins d'une semaine.", BODY))

    story.append(p(b("P1 — Actions immédiates (< 1 semaine) — Coût estimé : < 4h de travail"), H2))
    p1_data = [
        [b("Action"), b("Lien"), b("Impact ALE réduit"), b("Effort"), b("Méthode")],
        ["Activer TLS/HTTPS sur l'ALB",
         "ISO A.8.24\nNIST PR.DS-02\nFAIR F1",
         "−144 800 €/an",
         "2h",
         "AWS ACM : générer certificat gratuit → attacher à l'ALB listener 443 → rediriger 80→443"],
        ["Régénérer SECRET_KEY Flask",
         "ISO A.8.31\nNIST PR.DS-01\nFAIR F8",
         "−30 200 €/an",
         "30 min",
         "secrets.token_hex(32) → stocker dans AWS Secrets Manager → référencer dans l'app via boto3"],
        ["Ajouter headers sécurité HTTP",
         "ISO A.8.26\nNIST PR.PS-06\nPentest F3",
         "Réduction F3",
         "1h",
         "Flask: Strict-Transport-Security, X-Frame-Options, X-Content-Type-Options, CSP"],
        ["Sécuriser les cookies session",
         "ISO A.8.26\nPentest F4/F6",
         "Réduction F4/F6",
         "30 min",
         "SESSION_COOKIE_SECURE=True, SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax'"],
    ]
    story.append(Table(p1_data, colWidths=[3.5*cm, 2.2*cm, 2.5*cm, 1.2*cm, 5.6*cm],
                       style=table_style_header()))
    story.append(sp(0.2))

    story.append(p(b("P2 — Actions court terme (< 1 mois) — Gouvernance minimale"), H2))
    p2_data = [
        [b("Action"), b("Référentiel"), b("Livrable"), b("Effort estimé")],
        ["Politique de réponse aux incidents",   "ISO A.5.26\nNIST RS.*",   "Document 2 pages : détection → triage → escalade → post-mortem", "4h"],
        ["Registre des traitements RGPD Art.30", "RGPD A.30\nISO A.5.14",   "Tableau : traitement / base légale / durée / destinataires",       "2h"],
        ["Engagements de confidentialité",       "ISO A.6.6",                "NDA ou charte signée par chaque membre de l'équipe",              "1h"],
        ["Canal de signalement sécurité",        "ISO A.6.8\nNIST RS.CO-02","Adresse email dédiée ou ticket Jira — procédure écrite",           "1h"],
        ["Test de restauration RDS snapshot",    "NIST RC.RP-03",            "PV de test : snapshot → restore → vérification intégrité",        "2h"],
    ]
    story.append(Table(p2_data, colWidths=[4.5*cm, 2.5*cm, 6*cm, 2*cm],
                       style=table_style_header()))
    story.append(sp(0.2))

    story.append(p(b("P3 — Actions moyen terme (1–6 mois) — Maturité ISO 27001"), H2))
    p3_data = [
        [b("Action"), b("Référentiel"), b("Objectif"), b("Effort")],
        ["Politique d'utilisation acceptable des actifs", "ISO A.5.10",       "Couvrir les données clients et l'infra AWS",   "4h"],
        ["Séparation environnements dev/test/prod",       "ISO A.8.31",       "Comptes AWS distincts ou VPC isolés",          "8h"],
        ["Politique de gestion des mots de passe",        "ISO A.8.5\nF7",    "Longueur mini 12 car. + complexité + no reuse","2h"],
        ["Inventaire et classification des actifs",       "ISO A.5.9/A.5.12\nNIST ID.AM","Cartographie : app + BDD + S3 + EC2 + IAM",    "4h"],
        ["Clause sécurité fournisseur AWS",               "ISO A.5.19/A.5.20","Formaliser les responsabilités partagées AWS", "2h"],
        ["Plan de continuité documenté (PCA/PRI)",        "NIST RC.RP-01",    "Documenter : terraform apply comme PRA + RTO/RPO formels", "4h"],
    ]
    story.append(Table(p3_data, colWidths=[5*cm, 2.5*cm, 5*cm, 1.5*cm],
                       style=table_style_header()))
    story.append(PageBreak())

    # ─── 7. SYNTHÈSE ──────────────────────────────────────────────────────────
    story.append(p("7. SYNTHÈSE ET RECOMMANDATIONS", H1))
    story.append(sp(0.2))

    story.append(p(b("Tableau de bord GRC"), H2))
    dashboard = [
        [b("Référentiel"), b("Score actuel"), b("Cible"), b("Gap"), b("Verdict")],
        ["ISO 27001:2022", "1,72 / 5 (28% conformes)", "4,0 / 5 (90% conformes)", "−2,28",
         "Programme 12–18 mois"],
        ["NIST CSF 2.0",   "Tier 1 — 0,69 / 4",        "Tier 3 — 3,0 / 4",        "−2,31",
         "Actions immédiates RS/RC"],
        ["FAIR — ALE total","~192 000 € / an",          "< 30 000 € / an",          "−162 k€/an",
         "2 actions = −175 k€/an"],
        ["RGPD",           "Non conforme Art.30",        "Registre + DPO désigné",   "—",
         "Registre à créer"],
    ]
    ds = table_style_header()
    ds.add("BACKGROUND", (0,1), (-1,1), HexColor("#FADBD8"))
    ds.add("BACKGROUND", (0,2), (-1,2), HexColor("#FADBD8"))
    ds.add("BACKGROUND", (0,3), (-1,3), HexColor("#FEF9E7"))
    ds.add("BACKGROUND", (0,4), (-1,4), HexColor("#FADBD8"))
    story.append(Table(dashboard, colWidths=[3*cm, 4*cm, 3.5*cm, 1.5*cm, 3*cm],
                       style=ds))
    story.append(sp(0.3))

    story.append(p(b("Points forts identifiés"), H2))
    for pf in [
        "Architecture réseau — VPC Multi-AZ, subnets publics/privés, Security Groups en cascade, NACLs : conforme Defense in Depth.",
        "IAM et accès SSH — SSM Session Manager sans clé SSH, IAM roles avec moindre privilège : conforme A.8.2, A.8.18.",
        "Secrets management — AWS Secrets Manager pour les credentials BDD : conforme A.8.24 (partiellement).",
        "Chiffrement au repos — RDS chiffré, S3 SSE-S3, EBS chiffré : conforme A.8.24.",
        "Observabilité — CloudWatch (4 alarmes), GuardDuty, CloudTrail activés : bonne base de détection.",
        "WAF — Règles OWASP Core Rule Set, protection SQLi et rate limiting : conforme A.8.23.",
        "IaC Terraform — Infrastructure reproductible en 15 min : base du PRA (RTO 15 min).",
    ]:
        story.append(p(f"✓  {pf}", BULLET))
    story.append(sp(0.2))

    story.append(p(b("Points de risque persistants"), H2))
    for pr in [
        "HTTPS absent — l'unique vulnérabilité à impact financier le plus élevé (144 800 €/an). Correction : < 2h.",
        "SECRET_KEY Flask non sécurisée — forge de session possible. Correction : 30 minutes.",
        "Absence totale de gouvernance personnelle (A.6) — aucun engagement de confidentialité, aucune procédure RH.",
        "Absence de plan de réponse aux incidents — NIST RS score 0,23 — aucune procédure documentée.",
        "Absence de plan de reprise formalisé — NIST RC score 0,25 — terraform apply comme PRA non documenté.",
        "Registre RGPD Article 30 inexistant — obligation légale non remplie.",
        "Séparation dev/test/prod inexistante — même SECRET_KEY, même configuration.",
    ]:
        story.append(p(f"✗  {pr}", BULLET))
    story.append(sp(0.3))

    story.append(p(b("Priorisation ROI sécurité"), H2))
    roi_data = [
        [b("Action"), b("Coût estimé"), b("ALE réduit /an"), b("ROI annuel"), b("Délai")],
        ["TLS/HTTPS (ACM + ALB)",              "0 € (ACM gratuit) + 2h", "−144 800 €", "Immédiat", "< 1 jour"],
        ["SECRET_KEY → Secrets Manager",        "0 € + 30 min",          "− 30 200 €", "Immédiat", "< 1 jour"],
        ["Headers HTTP + cookies sécurisés",    "0 € + 1,5h",            "−Réduction F3/F4", "Immédiat", "< 1 jour"],
        ["Plan de réponse aux incidents (doc)", "4h rédaction",           "Couverture RS", "Court terme", "< 2 sem."],
        ["Registre RGPD Art.30",               "2h rédaction",           "Conformité légale", "Légal", "< 1 mois"],
    ]
    roi_t = table_style_header()
    roi_t.add("BACKGROUND", (0,1), (-1,1), HexColor("#D5F5E3"))
    roi_t.add("BACKGROUND", (0,2), (-1,2), HexColor("#D5F5E3"))
    roi_t.add("BACKGROUND", (0,3), (-1,3), HexColor("#EBF5FB"))
    story.append(Table(roi_data, colWidths=[4.5*cm, 3*cm, 2.8*cm, 2.2*cm, 2.5*cm],
                       style=roi_t))
    story.append(sp(0.4))

    story.append(hr())
    story.append(sp(0.2))
    story.append(p(
        b("Conclusion — ") +
        "L'infrastructure AWS de PixelStore présente une base technique solide : "
        "Defense in Depth, IAM moindre privilège, chiffrement au repos, WAF configuré. "
        "Les lacunes critiques sont concentrées sur trois axes : l'absence de TLS (risque financier dominant), "
        "l'absence totale de gouvernance organisationnelle et humaine (A.6), "
        "et l'absence de procédures de réponse et reprise après incident (RS/RC). "
        "Les deux premières actions correctives (TLS + SECRET_KEY) représentent moins de 3 heures de travail "
        "pour une réduction d'exposition de 175 000 €/an.", BODY))
    story.append(sp(0.3))

    foot = S("FootNote", fontSize=7, leading=10, textColor=HexColor("#888"), fontName="Helvetica-Oblique", alignment=TA_CENTER)
    story.append(p(
        "Rapport généré le 13 juin 2026 — GRC Agent Hermes (ISO 27001 gap analysis, NIST CSF 2.0 scoring, FAIR Monte Carlo 10 000 itérations) — "
        "Jedha Bootcamp Cybersécurité Fullstack", foot))

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"[+] PDF généré : {OUTPUT}")

if __name__ == "__main__":
    build()
