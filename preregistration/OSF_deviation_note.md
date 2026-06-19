# OSF deviation note — N_e calibration (2026-06-19)

**Registration:** https://osf.io/kp5jf  
**Lock date:** 2026-06-19  

## Change

Patient-level effective population size **N_e** is now **cohort-calibrated** to published Williams et al. 2016 / Dentro et al. 2021 median N_e anchors (`config/williams_Ne_reference.tsv`), implemented in `src/calibration.py`.

Raw site-frequency-spectrum estimates from cBioPortal VAFs were on an arbitrary scale (often 10⁶–10⁹), causing >90% of patients to appear above N_e* before calibration. Calibration preserves **within-cohort rank order** while mapping the cohort median to the literature anchor for each cancer type.

## Rationale

- Pre-registration specified N_e from standard sequencing outputs but did not fix absolute scale.
- Literature anchors are the intended clinical interpretability target.
- Fixed ε, δ, L table, and cohort list are **unchanged**.

## Impact on analyses

| Analysis | Effect |
|----------|--------|
| Cross-cancer ε* validation (Fig 2) | **Unchanged** — uses published N_e, V_A, L per type |
| TCGA PFS (Extended Data) | Re-run with calibrated N_e; binary split less imbalanced |
| BRAF targeted therapy (Fig 3) | Calibrated N_e; continuous Cox remains primary test |
| Clinical utility (Fig 4) | Distribution recentred; % above N_e* now varies by cohort |

## Files

- `config/williams_Ne_reference.tsv`
- `src/calibration.py`
- All `scripts/make_fig*.py` patient pipelines
