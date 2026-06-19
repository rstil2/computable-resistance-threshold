# Registration lock

| Field | Value |
|-------|-------|
| **OSF project** | https://osf.io/kp5jf |
| **Lock date** | 2026-06-19 |
| **Status** | Timestamped and locked on OSF |

## Frozen at lock (do not modify)

- `config/fixed_parameters.yaml` — ε, δ, endpoints, estimators
- `config/driver_loci_L.tsv` — independent L values
- `config/cohorts.yaml` — study IDs and inclusion/exclusion
- Analysis plan in `preregistration/OSF_registration_draft.md`

## Permitted after lock

- Bug fixes in code that do not change estimator definitions or constants
- Fetching/updating cBioPortal data (new patient records in same study IDs)
- Running pre-registered analyses (`scripts/03_fig2_km_analysis.py`, `scripts/04_fig3_cross_cancer.py`)
- Logging deviations in OSF deviations table if pre-specified contingency triggers (e.g. prostate PFS n < 100)

## Next analysis step

Wire real per-patient mutation VAFs into Fig 2 pipeline (replace placeholders in `scripts/03_fig2_km_analysis.py`), then run primary H1 log-rank on eligible cohorts.
