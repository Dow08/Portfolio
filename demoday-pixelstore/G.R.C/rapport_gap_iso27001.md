# Rapport Gap Analysis ISO 27001:2022

**Date** : 2026-06-13 12:18
**Contrôles évalués** : 93 / 93
**Contrôles implémentés (maturité ≥ 3)** : 26
**Score moyen de maturité** : 1.72 / 5
**Taux de couverture** : 100.0%
**Taux d'implémentation effective** : 28.0%

**Verdict global** : 🔴 Maturité faible - programme de mise en conformité de 12-18 mois

## Score par thème

| Thème | Contrôles évalués | Score moyen | % maturité ≥ 3 |
|---|---|---|---|
| Organisationnels (A.5) | 37 | 1.22 | 10.8% |
| Personnels (A.6) | 8 | 0.25 | 0.0% |
| Physiques (A.7) | 14 | 3.29 | 78.6% |
| Technologiques (A.8) | 34 | 1.97 | 32.4% |

## Écarts identifiés (à traiter en priorité)

| Code | Nom | Statut | Maturité | Thème | Commentaire |
|---|---|---|---|---|---|
| A.5.10 | Utilisation acceptable des actifs | Non implemente | 0 | Organisationnels (A.5) | Aucune politique d'utilisation acceptable des actifs |
| A.5.11 | Restitution des actifs | Non implemente | 0 | Organisationnels (A.5) | Pas de procedure de restitution des actifs |
| A.5.13 | Marquage de l'information | Non implemente | 0 | Organisationnels (A.5) | Pas de marquage de l'information |
| A.5.14 | Transfert d'information | Non implemente | 0 | Organisationnels (A.5) | Pas de politique de transfert d'information |
| A.5.19 | Sécurité dans relations fournisseurs | Non implemente | 0 | Organisationnels (A.5) | AWS comme fournisseur — pas de clause securite formalisee |
| A.5.20 | Sécurité dans accords fournisseurs | Non implemente | 0 | Organisationnels (A.5) | Pas d'accord de securite fournisseur documente |
| A.5.21 | Sécurité chaîne approvisionnement TIC | Non implemente | 0 | Organisationnels (A.5) | Chaine approvisionnement TIC non evaluee |
| A.5.25 | Évaluation et décision sur incidents | Non implemente | 0 | Organisationnels (A.5) | Pas de procedure d'evaluation et decision sur incidents |
| A.5.26 | Réponse aux incidents | Non implemente | 0 | Organisationnels (A.5) | Pas de procedure de reponse aux incidents documentee |
| A.5.28 | Collecte des preuves | Non implemente | 0 | Organisationnels (A.5) | Pas de procedure de collecte et preservation des preuves |
| A.5.32 | Droits de propriété intellectuelle | Non implemente | 0 | Organisationnels (A.5) | Droits propriete intellectuelle non evalues |
| A.5.36 | Conformité avec politiques | Non implemente | 0 | Organisationnels (A.5) | Pas de processus de verification de conformite aux politique |
| A.5.5 | Contact avec les autorités | Non implemente | 0 | Organisationnels (A.5) | Aucun contact etabli avec autorites (ANSSI/CNIL) |
| A.5.6 | Contact avec des groupes spécialisés | Non implemente | 0 | Organisationnels (A.5) | Aucune participation a des groupes specialises cybersecurite |
| A.6.1 | Vérification des antécédents | Non implemente | 0 | Personnels (A.6) | Pas de verification d'antecedents (contexte academique) |
| A.6.2 | Conditions d'embauche | Non implemente | 0 | Personnels (A.6) | Pas de conditions d'embauche avec clauses securite |
| A.6.4 | Processus disciplinaire | Non implemente | 0 | Personnels (A.6) | Pas de processus disciplinaire |
| A.6.5 | Responsabilités après emploi | Non implemente | 0 | Personnels (A.6) | Pas de procedures de sortie avec securite |
| A.6.6 | Engagements de confidentialité | Non implemente | 0 | Personnels (A.6) | Pas d'engagements de confidentialite signes |
| A.6.7 | Travail à distance | Non implemente | 0 | Personnels (A.6) | Pas de politique de travail a distance |
| A.6.8 | Signalement événements sécurité | Non implemente | 0 | Personnels (A.6) | Pas de canal de signalement des evenements de securite |
| A.7.7 | Bureau dégagé et écran verrouillé | Non implemente | 0 | Physiques (A.7) | Politique bureau propre non applicable / non definie |
| A.7.9 | Sécurité actifs hors site | Non implemente | 0 | Physiques (A.7) | Securite actifs hors site non definie |
| A.8.10 | Suppression de l'information | Non implemente | 0 | Technologiques (A.8) | Pas de politique de suppression des donnees |
| A.8.11 | Masquage de données | Non implemente | 0 | Technologiques (A.8) | Pas de masquage des donnees sensibles |
| A.8.12 | Prévention fuite données (DLP) | Non implemente | 0 | Technologiques (A.8) | Pas de DLP |
| A.8.19 | Installation logiciels systèmes opérationnels | Non implemente | 0 | Technologiques (A.8) | Pas de politique d'installation de logiciels |
| A.8.23 | Filtrage web | Non implemente | 0 | Technologiques (A.8) | Pas de filtrage web sortant depuis EC2 |
| A.8.30 | Développement externalisé | Non implemente | 0 | Technologiques (A.8) | Pas de processus de securite pour le dev externalise |
| A.8.33 | Informations de test | Non implemente | 0 | Technologiques (A.8) | Pas de politique de gestion des donnees de test |

*... et 37 autres écarts (voir CSV complet)*


## Plan d'action recommandé

1. **Traiter les contrôles de maturité 0 ou 1** : ce sont les écarts majeurs.
2. **Consolider les contrôles de maturité 2** : formaliser et documenter.
3. **Optimiser les contrôles de maturité 3** : mesurer et améliorer.
4. **Compléter les contrôles non évalués** sous 30 jours.
5. **Revue dans 3 mois** après plan d'action initial.

## Méthodologie

- Échelle CMMI : 0 (inexistant) → 5 (optimisé)
- Seuil de conformité visé : maturité ≥ 3 sur 90% des contrôles applicables
- Réévaluation : annuelle minimum, ou après changement majeur du périmètre.
