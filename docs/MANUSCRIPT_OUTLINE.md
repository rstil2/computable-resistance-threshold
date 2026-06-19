# Manuscript outline — Nature Cancer / Nature Communications

**Title:** A computable threshold below which tumours cannot evolve drug resistance

**Target:** Nature Cancer (primary) · Nature Communications (parallel)

**No wet lab.** Causal Fig 4/5 dropped. OSF: https://osf.io/kp5jf

---

## Abstract (~150 words)

1. Resistance dominates treatment failure and appears unpredictable.
2. We define N_e*, a resistance-learnability threshold computable from standard sequencing (V_A, N_e, driver-panel L).
3. Across **17 cancer types**, theoretical ε* tracks resistance durability (Pearson r = 0.88, LOO min r = 0.77).
4. In the best available targeted-therapy cohort (BRAF inhibitor, n = 45), continuous log(N_e/N_e*) does **not** predict duration (Cox p = 0.97) — underpowered but pre-specified.
5. Most sequencing reports already contain the inputs; N_e* offers a pre-treatment risk stratifier — not yet a treatment algorithm.

---

## Main figures (revised numbering)

| Fig | Title | Source |
|-----|-------|--------|
| 1 | Concept + sequencing report mapping | `scripts/make_fig1_clinical.py` → `data/fig1/` |
| 2 | Cross-cancer ε* validation (17 types) | `scripts/make_fig2_cross_cancer.py` → `data/fig2_cross_cancer/` |
| 3 | Patient-level targeted therapy (BRAF) | `scripts/make_fig3_targeted.py` → `data/fig3_targeted/` |
| 4 | Clinical utility (% above N_e* by type) | `scripts/make_fig4_utility.py` → `data/fig4_utility/` |

**Extended Data:** `scripts/make_ed_tcga_null.py` · L sensitivity (`fig2_cross_cancer/L_sensitivity.csv`) · theory note · immune panel

---

## Results section order

1. **N_e* is computable at diagnosis** (Fig 1)
2. **Threshold predicts resistance ecology across cancers** (Fig 2) — *main quantitative result*
3. **Patient-level association on targeted therapy** (Fig 3) — *best available clinical endpoint*
4. **Population-level utility** (Fig 4)
5. **Limitations:** no causal manipulation; adjuvant/mixed cohorts; pre-registered TCGA PFS null (ED)

---

## What we do NOT claim

- We do not claim to have experimentally manipulated N_e.
- We do not claim organoid/PDX benefit without data.
- We do not claim binary N_e* stratification works on generic PFS (tested, null).

---

## Immediate build queue

See `docs/STATUS.md` for live results.

1. ~~Expand cross-cancer types (Fig 2)~~
2. ~~BRAF targeted patient Cox (Fig 3)~~ — null documented
3. ~~Calibrate N_e estimator~~
4. ~~Fig 1 clinical mock-up + utility panel~~
5. ~~Run Extended Data TCGA script + draft Introduction / Results~~ — Results + abstract drafted (`docs/MANUSCRIPT_*_draft.md`)
