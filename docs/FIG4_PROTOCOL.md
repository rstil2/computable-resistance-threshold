# Fig 4 — Laboratory protocol (collaborator-ready)

**Title:** Causal test of the resistance-learnability threshold N_e*  
**OSF:** https://osf.io/kp5jf (locked 2026-06-19)  
**Contact:** R. Craig Stillwell

---

## Hypothesis (Fig 4)

If resistance evolution requires effective population size N_e ≥ N_e*, then **manipulating bottleneck N_e** at fixed drug selection should produce a **sharp increase** in resistance emergence at N_e ≈ N_e* — not a smooth dose–response in population size.

---

## Systems (minimum n = 2)

| ID | Cell line | Drug | N_e* inputs (parental) |
|----|-----------|------|------------------------|
| EGFR_PC9 | PC9 (EGFR ex19del) | Osimertinib 3rd-gen TKI | L = 12, V_A = 0.09 |
| BRAF_A375 | A375 (BRAF V600E) | Vemurafenib | L = 10, V_A = 0.14 |

Compute N_e* from parental WES before starting (`src/threshold.py` or project spreadsheet). **Record N_e* and lock before randomizing cultures to arms.**

---

## Experimental arms (6 × 8 replicates = 48 cultures per system)

Bottleneck effective population at each passage:

| Arm | N_e target | Purpose |
|-----|------------|---------|
| 1 | 0.05 × N_e* | Deeply sub-threshold |
| 2 | 0.20 × N_e* | Sub-threshold |
| 3 | 0.50 × N_e* | Near threshold (below) |
| 4 | 1.00 × N_e* | At threshold |
| 5 | 2.00 × N_e* | Supra-threshold |
| 6 | 10.0 × N_e* | Positive control (should resist) |

**Drug:** IC80 for each line (determined once, then **identical across all arms**).  
**Passages:** 14 selection cycles (~21 days, 36 h/passage).  
**Bottleneck:** Exact cell count passaged each cycle (e.g. FACS or limiting dilution to target N_e).

---

## Barcoding

1. Transduce parental line with lentiviral barcode library (≥10⁶ diversity; MOI 0.1 so ~1 barcode/cell).
2. Expand 72 h; confirm >80% marked.
3. Aliquot into 48 independent cultures per system (8 reps × 6 arms).
4. Sample every 3 days: gDNA → PCR barcode amplicon → Illumina (≥50k reads/culture).

**N_e verification:** Shannon effective number of barcodes at bottleneck should match target ±20%.

---

## Resistance readouts (day 21)

**Primary (either suffices):**

1. **Molecular:** Amplicon seq gatekeeper panel  
   - PC9: EGFR T790M, MET amp, ERBB2, BRAF, PIK3CA  
   - A375: NRAS Q61, MAP2K1 K57, CRAF, PTEN loss  

2. **Functional:** IC50 on collected cells vs parental; **≥3× shift** on same drug.

Binary `resistance` = 1 if molecular OR functional positive.

---

## Randomization & blinding

- Randomize culture IDs to arms; resistance caller blinded to arm until database lock.
- Parental N_e* computed by analyst not performing daily culture work.

---

## Primary analysis (pre-registered)

- Logistic regression: `resistance ~ log10(N_e / N_e*)`
- Changepoint test at log10 ratio = 0 (N_e = N_e*)
- Figure: P(resistance) vs log10(N_e/N_e*) with 95% CI per arm

**Script:** `scripts/06_fig4_make_figure.py`  
**Data file:** save as `data/fig4/lab_results.csv` (see `lab_results_TEMPLATE.csv`)

---

## Timeline

| Week | Task |
|------|------|
| 1 | Parental WES; compute N_e*; IC80; barcode transduction |
| 2 | Arm setup; begin selection |
| 3–4 | Passage + sampling |
| 5 | Resistance assays; upload CSV; run analysis script |

---

## Budget sketch (USD)

| Item | Est. |
|------|------|
| Barcode library + sequencing | $8–15k |
| Cell culture / drug | $3–5k |
| Amplicon resistance panels | $4–6k |
| **Total per 2-line study** | **~$15–25k** |

---

## Success criteria

- Changepoint at N_e/N_e* = 1 supported (Chow p < 0.05 OR piecewise AIC beats single logistic by ≥4)
- Low arms (0.05–0.5 × N_e*): P(resist) < 0.25 pooled
- High arms (2–10 × N_e*): P(resist) > 0.60 pooled
- Replicated in both PC9 and A375

---

## Files in this repo

```
config/fig4_experiment.yaml     ← locked arm design
scripts/05_fig4_power.py        ← power check
scripts/06_fig4_make_figure.py  ← figure + stats
docs/FIG4_PROTOCOL.md           ← this file
data/fig4/lab_results_TEMPLATE.csv
```

When lab data exist: copy template → `lab_results.csv`, re-run script 06.
