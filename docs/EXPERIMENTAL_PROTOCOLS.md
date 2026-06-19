# Experimental protocols — Figs 4 & 5 (collaborator-facing)

## Fig 4 — Causal threshold (barcoded cell-line evolution)

**Prediction:** Probability of resistance emergence collapses sharply below predicted \(N_e^*\), not as a smooth gradient.

### Design

| Arm | Bottleneck \(N_e\) | Drug dose | Replicates |
|-----|-------------------|-----------|------------|
| 1 | 0.05 × \(N_e^*\) | Fixed IC80 | ≥6 |
| 2 | 0.2 × \(N_e^*\) | Fixed IC80 | ≥6 |
| 3 | 0.5 × \(N_e^*\) | Fixed IC80 | ≥6 |
| 4 | 1.0 × \(N_e^*\) | Fixed IC80 | ≥6 |
| 5 | 2.0 × \(N_e^*\) | Fixed IC80 | ≥6 |
| 6 | 10 × \(N_e^*\) | Fixed IC80 | ≥6 |

- **Cell lines:** ≥2 (e.g. EGFR-mutant PC9 or HCC827; BRAF V600E A375 or WM793)
- **Drugs:** Matched targeted agents (osimertinib; vemurafenib ± cobimetinib)
- **Barcoding:** Lentiviral diversity ≥10⁶; lineage tracking every 3 days
- **Resistance readout:** Molecular (gatekeeper mutation by amplicon seq) + functional (IC50 shift >3×)
- **\(N_e^*\) prediction:** Compute from baseline WES of parental line (V_A, L from driver panel)

### Primary statistic

Logistic regression: `resistance ~ bottleneck_Ne + offset(log(Ne/N_e*))` with changepoint test at \(N_e = N_e^*\).

### Replication

Repeat full arm matrix for second drug/line pair.

---

## Fig 5 — Therapeutic implication (organoid / PDX)

**Prediction:** Resistance prevented only when combination maintains \(N_e < N_e^*\) at matched total cytotoxicity.

### Arms (matched viability at 72h)

| Arm | Regimen | Intent |
|-----|---------|--------|
| A | Targeted monotherapy → switch at progression | Standard sequential (control) |
| B | Upfront double block (same targets) | Suppress \(N_e\) below \(N_e^*\) |
| C | Upfront combo at sub-cytotoxic dose | Negative control (insufficient \(N_e\) suppression) |

### Readouts

- Live \(N_e\) proxy: ctDNA VAF sum or organoid cell count + subclone tracking
- Time to resistance mutation (same panel as Fig 4)
- Total cell kill matched ±10% across arms

### Confound control

Same targeted agents in A vs B; do not compare TKI monotherapy to unrelated chemotherapy combo.

---

## Venue path

| Stage | Figures | Target |
|-------|---------|--------|
| Now | 1–3 | Nature Cancer / Nat Commun |
| + Fig 4 | 1–4 | Nature / Science |
| + Fig 5 | 1–5 | Complete package |
