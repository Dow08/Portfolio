# Quantification FAIR - Forge de session via SECRET_KEY faible (F8 pentest)

**Date** : 2026-06-13 12:18
**Itérations Monte Carlo** : 10,000
**Description** : Si la SECRET_KEY Flask est triviale, un attaquant peut forger des cookies et usurper n'importe quel compte

## Hypothèses (PERT 3 points)

| Facteur | Min | Likely | Max |
|---|---|---|---|
| TEF | 0.100 | 0.500 | 2.000 |
| Vuln | 0.200 | 0.400 | 0.700 |
| PLM_par_evenement | 5.0 k€ | 30.0 k€ | 100.0 k€ |
| SLM_par_evenement | 10.0 k€ | 50.0 k€ | 200.0 k€ |

## Résultats - Annual Loss Expectancy (ALE)

| Statistique | Valeur |
|---|---|
| Moyenne | 30.2 k€ |
| Médiane (P50) | 25.4 k€ |
| P75 | 39.8 k€ |
| **P90** | **57.2 k€** |
| **P95** | **70.7 k€** |
| P99 | 100.0 k€ |
| Maximum simulé | 185.9 k€ |
| Écart-type | 20.5 k€ |

## Loss Event Frequency (LEF)

- Moyenne : 0.285 événements/an
- Médiane : 0.258 événements/an
- P90 : 0.500 événements/an

## Loss Magnitude par événement (LM)

- Moyenne : 106.0 k€
- Médiane : 102.4 k€
- P90 : 156.5 k€

## Distribution ALE (histogramme)

```
      1.2 k€ | █████████████ 349
      6.1 k€ | ██████████████████████████████████████ 1015
     11.1 k€ | ██████████████████████████████████████████████████ 1312
     16.0 k€ | █████████████████████████████████████████████████ 1286
     20.9 k€ | ███████████████████████████████████████████ 1137
     25.9 k€ | ██████████████████████████████████████ 1006
     30.8 k€ | ████████████████████████████████ 841
     35.8 k€ | █████████████████████████ 672
     40.7 k€ | ███████████████████ 504
     45.7 k€ | ████████████████ 438
     50.6 k€ | ████████████ 341
     55.5 k€ | █████████ 261
     60.5 k€ | ███████ 185
     65.4 k€ | █████ 143
     70.4 k€ | █████ 135
     75.3 k€ | ███ 98
     80.3 k€ | ██ 70
     85.2 k€ | █ 51
     90.2 k€ | █ 27
     95.1 k€ | █ 30
```

## Interprétation

- **Perte annuelle moyenne attendue** : 30.2 k€
- **Dans 90% des cas**, la perte annuelle sera **inférieure à 57.2 k€**.
- **Pire scénario crédible (P95)** : 70.7 k€
- **Cas extrême (P99)** : 100.0 k€

## Recommandations

- Présenter à la Direction la **valeur P90** comme référence de budget de défense.
- Comparer le coût d'une mesure de réduction du risque à la **différence d'ALE moyen** avant/après.
- Une mesure n'est pertinente que si elle réduit l'ALE de plus que son coût total de possession.
- Réviser le scénario annuellement, ou après un incident significatif modifiant les hypothèses.

## Méthodologie

- Modèle FAIR : ALE = LEF × LM avec LEF = TEF × Vuln et LM = PLM + SLM.
- Distribution PERT-Beta (gamma=4) sur chaque facteur, échantillonnée en Monte Carlo.
- Cohérent avec les pratiques The Open Group O-RT (Risk Taxonomy) et O-RA (Risk Analysis).