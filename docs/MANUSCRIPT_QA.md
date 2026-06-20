# Manuscript QA audit (2026-06-19)

Internal checklist after elevated editorial pass. Numbers verified against `data/*/summary.csv` and related outputs.

## Statistics verified ✓

| Claim | Source | Value in text |
|-------|--------|---------------|
| Cross-cancer Pearson r | fig2_cross_cancer/summary.csv | 0.88 (raw 0.881) |
| Cross-cancer P | same | 3.1 × 10⁻⁶ |
| LOO min r | same | 0.77 |
| Bootstrap 95% CI | same | 0.51–0.96 |
| L sensitivity r | L_sensitivity.csv | 0.879 / 0.881 / 0.880 |
| BRAF Cox HR (95% CI) | fig3_targeted/analysis_summary.csv | 0.97 (0.20–4.71) |
| BRAF Cox P | same | 0.97 |
| BRAF Spearman ρ | same | −0.025, P = 0.87 |
| BRAF logistic OR | same | 0.84, P = 0.86 |
| BRAF n / events | same | 45 / 14 |
| Below N_e* | braf_patients.csv | 44 / 45 |
| Utility n | fig4 cohorts | 1564 (528+433+557+46) |
| Utility % above | summary_by_cohort.csv | 20, 28, 2, 2% |
| TCGA pooled n | ed_tcga/km_cox_summary.csv | 1440 |
| TCGA % above | same | 16.2% (233/1440) |
| TCGA log-rank P | same | 0.55 |
| TCGA Cox HR/P pooled | same | 0.82, P = 0.042 |
| Fig 1 example N_e* | make_fig1_clinical.py run | 9262, ratio 0.89 |

## Corrections made in editorial pass

1. **Removed repository file paths** from Results/Methods main text (`config/...`, `data/...`) — replaced with Extended Data / Supplementary / code repository references.
2. **Removed “Project 51 working directory”** from Methods.
3. **Clarified title claim** in Discussion: “cannot evolve” = PAC learnability sense, not empirical proof.
4. **Fixed abstract wording**: “manipulability” → causal manipulation; added Cox CI.
5. **Single author consistency**: “The author declares…” competing interests; acknowledgements singular.
6. **Bootstrap CI** now interpreted explicitly (uncertainty from n = 17 types).
7. **TCGA Cox P = 0.042** reported to three significant figures consistently (was 0.04).
8. **Extended Data Table 3** r values aligned to L_sensitivity.csv (0.879–0.881).
9. **Added Valiant (1984)** PAC learning reference.
10. **Van Allen et al. 2014** explicitly tied to Broad BRAF cohort.

## Remaining items before submission

- [ ] **Affiliation** in `manuscript/content.py` (`AFFILIATION`)
- [ ] **Funding** in acknowledgements
- [ ] **Supplementary Note 1** (theory) as separate PDF — referenced but not bundled in repo
- [ ] **Supplementary Table 1** (full cross-cancer sources) — export from cross_cancer_table.csv to formatted table
- [ ] Zenodo DOI at acceptance
- [ ] OSF: link GitHub repo on project page
- [ ] Consider whether title “cannot evolve” will pass editorial review without subtitle — Discussion now defines scope

## Known limitations (correctly stated in paper)

- Patient BRAF test is underpowered and 98% below N_e* after calibration.
- TCGA continuous Cox significant but **wrong direction** — labelled negative control / endpoint mismatch.
- Cross-cancer TTR₂ values are literature aggregates, not a single protocol.
- N_e calibration is post-registration (OSF deviation note filed).

## Figure–text consistency ✓

- Fig 1: N_e* = 9,262; ratio 0.89; below threshold
- Fig 2: 17 types; r = 0.88
- Fig 3: n = 45; null Cox
- Fig 4: n = 1,564; cohort percentages match summary CSV
- ED Fig 1: n = 1,440; P = 0.55
