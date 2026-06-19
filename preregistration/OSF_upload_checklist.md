# OSF upload checklist (manual steps)

**Project:** https://osf.io/kp5jf  
**Lock date:** 2026-06-19  

You must complete these in the OSF web UI (no API token in this repo).

## 1. Deviation note (N_e calibration)

- [ ] Upload `preregistration/OSF_deviation_note.md` to the OSF project Files  
- [ ] Add a one-line note on the registration: *"2026-06-19 addendum: patient N_e cohort-calibrated to Williams 2016 medians; ε, δ, L, cohorts unchanged."*

## 2. Analysis code snapshot

- [ ] Upload zip of `config/`, `src/`, `scripts/make_fig*.py`, `scripts/run_nat_cancer_figures.py`, `requirements.txt`  
  **or** link https://github.com/rstil2/computable-resistance-threshold  

## 3. Key result tables (optional but reviewer-friendly)

- [ ] `data/fig2_cross_cancer/cross_cancer_table.csv`  
- [ ] `data/fig2_cross_cancer/summary.csv`  
- [ ] `data/fig3_targeted/braf_patients.csv`  
- [ ] `data/ed_tcga/km_cox_summary.csv`  

## 4. Figure PDFs at submission

- [ ] `data/fig1/` through `data/fig4_utility/`  
- [ ] `data/ed_tcga/ed_tcga_pfs_km.pdf`  

## 5. Do not change without new deviation log

- `config/fixed_parameters.yaml` — ε, δ  
- `config/driver_loci_L.tsv` — L table  
- `config/cohorts.yaml` — primary cohort list  
