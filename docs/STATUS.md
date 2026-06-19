# Project 51 — where things stand

**Paper:** A computable threshold below which tumours cannot evolve drug resistance  
**Target:** Nature Cancer / Nature Communications (no wet lab)  
**OSF (locked):** https://osf.io/kp5jf  
**Lock date:** 2026-06-19  

---

## One-sentence thesis (revised)

At diagnosis, compute **N_e\*** from sequencing. It tracks resistance ecology across cancer types; on targeted therapy with resistance-specific endpoints, test whether **log(N_e/N_e\*)** associates with treatment failure.

---

## Five strengthening items — status

| # | Item | Status | Output |
|---|------|--------|--------|
| 1 | Expand cross-cancer validation (Fig 2) | **Done** | 17 types, r=0.88, LOO min r=0.77 |
| 2 | Targeted-therapy patient Cox (Fig 3) | **Done (null)** | BRAF Broad n=45; Cox p≈0.97; MSK BRAF lacks outcome fields |
| 3 | N_e calibration to Williams medians | **Done** | `src/calibration.py`; OSF deviation note filed |
| 4 | Fig 1 clinical mock-up | **Done** | `data/fig1/fig1_clinical_report.pdf` |
| 5 | Clinical utility panel (Fig 4) | **Done** | `data/fig4_utility/` |

**Re-run all main figures:**
```bash
cd "/Users/stillwell/Documents/Google Drive/Project 51 - Cancer Ne"
MPLCONFIGDIR="$(pwd)/.mpl" .venv/bin/python scripts/run_nat_cancer_figures.py
```

**Extended Data (TCGA PFS null, calibrated):**
```bash
.venv/bin/python scripts/make_ed_tcga_null.py
```

---

## Key results (2026-06-19)

### Fig 2 — cross-cancer (main empirical spine)
- Pearson **r = 0.88** (p ≈ 3×10⁻⁶), **n = 17** cancer types
- LOO mean r = 0.88, **min r = 0.77**
- L sensitivity: r stable at 0.5×–2× L multipliers
- `data/fig2_cross_cancer/`

### Fig 3 — BRAF inhibitor (Broad 2012)
- n = 45, 14 events; **44/45 below N_e\*** after calibration
- Cox HR = 0.97 (0.20–4.71), **p = 0.97** — pre-registered H2 **not met**
- Honest null; paper frames as “best available resistance endpoint, underpowered”
- MSK BRAF 2024 cohorts (n≈210) have **no duration/resistance fields** in cBioPortal
- `data/fig3_targeted/`

### Fig 4 — clinical utility
| Cohort | n | % above N_e* | Median N_e/N_e* |
|--------|---|--------------|-----------------|
| Colorectal | 528 | 20% | 0.48 |
| Melanoma (TCGA) | 433 | 28% | 0.56 |
| Melanoma (BRAF) | 46 | 2% | 0.18 |
| NSCLC | 557 | 2% | 0.24 |

### Extended Data — TCGA generic PFS (calibrated N_e)
- Pooled n = 1440; **16% above N_e\*** (calibration fixed prior 94% imbalance)
- Binary log-rank **p = 0.55** (null)
- Continuous Cox HR = 0.82, p = 0.04 — **wrong direction** vs H2; generic PFS confounded; cite as pre-registered sensitivity only
- `data/ed_tcga/ed_tcga_pfs_km.pdf`, `km_cox_summary.csv`

---

## Folder map

```
Project 51 - Cancer Ne/
├── config/              ← locked constants + Williams N_e anchors
├── preregistration/     ← OSF + OSF_deviation_note.md (N_e calibration)
├── scripts/
│   make_fig1_clinical.py
│   make_fig2_cross_cancer.py   ← main Fig 2
│   make_fig3_targeted.py       ← main Fig 3
│   make_fig4_utility.py        ← main Fig 4
│   make_ed_tcga_null.py        ← Extended Data
│   run_nat_cancer_figures.py
├── data/
│   fig1/ fig2_cross_cancer/ fig3_targeted/ fig4_utility/
│   ed_tcga/   (after ED script)
│   fig2/      ← legacy TCGA KM (uncalibrated)
└── docs/
    NAT_CANCER_PLAN.md
    MANUSCRIPT_OUTLINE.md
```

---

## Next milestones

1. ~~**Run Extended Data script**~~ — done (`data/ed_tcga/`)
2. ~~**Draft Results**~~ — `docs/MANUSCRIPT_RESULTS_draft.md`
3. **Upload OSF deviation note** — checklist: `preregistration/OSF_upload_checklist.md`
4. **GitHub/Zenodo release** — guide: `docs/REPRODUCIBILITY.md`
5. ~~**Draft Introduction + Discussion**~~ — included in `manuscript/MANUSCRIPT_draft.docx`
5. ~~**Fill author names**, references, GitHub/Zenodo URL in docx~~ — template in `manuscript/content.py`; complete draft built
6. **Your edits:** author list, funding, Zenodo DOI at acceptance
7. **Optional:** TRACERx EGA bonus; supplementary theory note PDF

---

## What we do NOT claim

- No causal N_e manipulation (wet lab dropped)
- No organoid/PDX benefit without data
- No binary N_e* stratification on generic TCGA PFS as headline result

---

*Updated: 2026-06-19*
