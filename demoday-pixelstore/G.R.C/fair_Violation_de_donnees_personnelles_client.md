# Quantification FAIR - Violation de donnees personnelles clients (RGPD — notification CNIL)

**Date** : 2026-06-13 12:18
**Itérations Monte Carlo** : 10,000
**Description** : Fuite BDD RDS contenant emails + mots de passe : obligation notification CNIL 72h + clients

## Hypothèses (PERT 3 points)

| Facteur | Min | Likely | Max |
|---|---|---|---|
| TEF | 0.050 | 0.200 | 1.000 |
| Vuln | 0.100 | 0.250 | 0.500 |
| PLM_par_evenement | 10.0 k€ | 50.0 k€ | 200.0 k€ |
| SLM_par_evenement | 20.0 k€ | 80.0 k€ | 500.0 k€ |

## Résultats - Annual Loss Expectancy (ALE)

| Statistique | Valeur |
|---|---|
| Moyenne | 17.0 k€ |
| Médiane (P50) | 13.4 k€ |
| P75 | 22.2 k€ |
| **P90** | **33.7 k€** |
| **P95** | **43.2 k€** |
| P99 | 64.3 k€ |
| Maximum simulé | 130.5 k€ |
| Écart-type | 13.3 k€ |

## Loss Event Frequency (LEF)

- Moyenne : 0.081 événements/an
- Médiane : 0.070 événements/an
- P90 : 0.150 événements/an

## Loss Magnitude par événement (LM)

- Moyenne : 208.2 k€
- Médiane : 195.4 k€
- P90 : 326.6 k€

## Distribution ALE (histogramme)

```
       771 € | ██████████████████████ 708
      3.9 k€ | ███████████████████████████████████████████████ 1474
      7.1 k€ | ██████████████████████████████████████████████████ 1550
     10.3 k€ | ██████████████████████████████████████████ 1311
     13.5 k€ | ███████████████████████████████████ 1111
     16.6 k€ | ███████████████████████████ 839
     19.8 k€ | █████████████████████ 681
     23.0 k€ | █████████████████ 536
     26.2 k€ | ████████████ 395
     29.3 k€ | █████████ 300
     32.5 k€ | ███████ 232
     35.7 k€ | █████ 172
     38.9 k€ | ████ 142
     42.0 k€ | ███ 118
     45.2 k€ | ██ 78
     48.4 k€ | ██ 84
     51.6 k€ | ██ 65
     54.7 k€ | █ 48
     57.9 k€ |  30
     61.1 k€ |  27
```

## Interprétation

- **Perte annuelle moyenne attendue** : 17.0 k€
- **Dans 90% des cas**, la perte annuelle sera **inférieure à 33.7 k€**.
- **Pire scénario crédible (P95)** : 43.2 k€
- **Cas extrême (P99)** : 64.3 k€

## Recommandations

- Présenter à la Direction la **valeur P90** comme référence de budget de défense.
- Comparer le coût d'une mesure de réduction du risque à la **différence d'ALE moyen** avant/après.
- Une mesure n'est pertinente que si elle réduit l'ALE de plus que son coût total de possession.
- Réviser le scénario annuellement, ou après un incident significatif modifiant les hypothèses.

## Méthodologie

- Modèle FAIR : ALE = LEF × LM avec LEF = TEF × Vuln et LM = PLM + SLM.
- Distribution PERT-Beta (gamma=4) sur chaque facteur, échantillonnée en Monte Carlo.
- Cohérent avec les pratiques The Open Group O-RT (Risk Taxonomy) et O-RA (Risk Analysis).