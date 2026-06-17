# Quantification FAIR - Interception credentials clients (HTTP en clair — F1 pentest)

**Date** : 2026-06-13 12:18
**Itérations Monte Carlo** : 10,000
**Description** : Absence de TLS/HTTPS : credentials utilisateurs interceptables en clair sur reseau non securise

## Hypothèses (PERT 3 points)

| Facteur | Min | Likely | Max |
|---|---|---|---|
| TEF | 0.500 | 2.000 | 8.000 |
| Vuln | 0.600 | 0.800 | 0.950 |
| PLM_par_evenement | 2.0 k€ | 15.0 k€ | 80.0 k€ |
| SLM_par_evenement | 5.0 k€ | 25.0 k€ | 150.0 k€ |

## Résultats - Annual Loss Expectancy (ALE)

| Statistique | Valeur |
|---|---|
| Moyenne | 144.8 k€ |
| Médiane (P50) | 123.0 k€ |
| P75 | 192.6 k€ |
| **P90** | **275.0 k€** |
| **P95** | **331.6 k€** |
| P99 | 448.2 k€ |
| Maximum simulé | 792.1 k€ |
| Écart-type | 95.2 k€ |

## Loss Event Frequency (LEF)

- Moyenne : 2.174 événements/an
- Médiane : 2.030 événements/an
- P90 : 3.644 événements/an

## Loss Magnitude par événement (LM)

- Moyenne : 66.4 k€
- Médiane : 63.0 k€
- P90 : 104.5 k€

## Distribution ALE (histogramme)

```
      5.9 k€ | ████████████ 295
     28.0 k€ | █████████████████████████████████████████ 966
     50.1 k€ | ██████████████████████████████████████████████████ 1176
     72.2 k€ | █████████████████████████████████████████████████ 1156
     94.3 k€ | ██████████████████████████████████████████████ 1093
    116.5 k€ | ████████████████████████████████████████ 954
    138.6 k€ | █████████████████████████████████████ 886
    160.7 k€ | █████████████████████████████ 703
    182.8 k€ | ████████████████████████ 578
    204.9 k€ | ███████████████████ 465
    227.0 k€ | ███████████████ 354
    249.1 k€ | █████████████ 322
    271.3 k€ | █████████ 234
    293.4 k€ | ████████ 198
    315.5 k€ | ██████ 158
    337.6 k€ | █████ 132
    359.7 k€ | ███ 80
    381.8 k€ | ██ 56
    404.0 k€ | ██ 57
    426.1 k€ | █ 38
```

## Interprétation

- **Perte annuelle moyenne attendue** : 144.8 k€
- **Dans 90% des cas**, la perte annuelle sera **inférieure à 275.0 k€**.
- **Pire scénario crédible (P95)** : 331.6 k€
- **Cas extrême (P99)** : 448.2 k€

## Recommandations

- Présenter à la Direction la **valeur P90** comme référence de budget de défense.
- Comparer le coût d'une mesure de réduction du risque à la **différence d'ALE moyen** avant/après.
- Une mesure n'est pertinente que si elle réduit l'ALE de plus que son coût total de possession.
- Réviser le scénario annuellement, ou après un incident significatif modifiant les hypothèses.

## Méthodologie

- Modèle FAIR : ALE = LEF × LM avec LEF = TEF × Vuln et LM = PLM + SLM.
- Distribution PERT-Beta (gamma=4) sur chaque facteur, échantillonnée en Monte Carlo.
- Cohérent avec les pratiques The Open Group O-RT (Risk Taxonomy) et O-RA (Risk Analysis).