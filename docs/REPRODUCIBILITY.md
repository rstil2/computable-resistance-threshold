# Reproducibility — GitHub / Zenodo bundle

This document describes what to publish alongside the manuscript and how to reproduce all figures.

## What to archive

| Path | Purpose |
|------|---------|
| `config/` | Locked ε, δ, L table, cohorts, Williams N_e anchors |
| `src/` | N_e\*, estimators, cBioPortal client, calibration |
| `scripts/make_fig*.py`, `scripts/make_ed_tcga_null.py`, `scripts/run_nat_cancer_figures.py` | Figure pipelines |
| `requirements.txt` | Python dependencies |
| `preregistration/OSF_deviation_note.md` | Post-lock N_e calibration deviation |
| `data/fig*/`, `data/ed_tcga/` | Generated outputs (optional in repo; regenerate from cache) |
| `data/cache/` | cBioPortal JSON caches (~large; Zenodo OK, Git LFS optional) |

**Repository:** https://github.com/rstil2/computable-resistance-threshold

## One-command figure reproduction

```bash
cd "/path/to/Project 51 - Cancer Ne"
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# First run downloads mutations (~5 min); cached under data/cache/
export MPLCONFIGDIR="$(pwd)/.mpl"
python scripts/run_nat_cancer_figures.py
```

Outputs:

| Figure | PDF path |
|--------|----------|
| Fig. 1 | `data/fig1/fig1_clinical_report.pdf` |
| Fig. 2 | `data/fig2_cross_cancer/fig2_cross_cancer.pdf` |
| Fig. 3 | `data/fig3_targeted/fig3_targeted_therapy.pdf` |
| Fig. 4 | `data/fig4_utility/fig4_clinical_utility.pdf` |
| ED TCGA | `data/ed_tcga/ed_tcga_pfs_km.pdf` |

Summary tables: `data/fig2_cross_cancer/summary.csv`, `data/fig3_targeted/analysis_summary.csv`, `data/fig4_utility/summary_by_cohort.csv`, `data/ed_tcga/km_cox_summary.csv`.

## OSF linkage

1. **Registration (locked):** https://osf.io/kp5jf  
2. **Upload deviation note:** `preregistration/OSF_deviation_note.md` as a project file or registration addendum.  
3. **Link GitHub/Zenodo** in OSF project description and manuscript Data Availability.  
4. **Tag release** at submission (e.g. `v1.0-natcancer-submission`) with DOI from Zenodo.

## Zenodo checklist

- [ ] Create release tarball or connect GitHub repo  
- [ ] Title: *Code for: A computable threshold below which tumours cannot evolve drug resistance*  
- [ ] Authors match manuscript  
- [ ] License: MIT or CC-BY-4.0 (choose before upload)  
- [ ] Include `CITATION.cff` (optional) pointing to manuscript when available  

## Environment

- Python ≥ 3.11  
- Tested on macOS 2026-06-19  
- Network required for first cBioPortal fetch only  
