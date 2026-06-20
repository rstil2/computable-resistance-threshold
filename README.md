# N_e*: a computable population-size threshold for resistance learnability from standard tumour sequencing

**Author:** R. Craig Stillwell, Independent Scholar (craig.stillwell@gmail.com)  
**Code:** https://github.com/rstil2/computable-resistance-threshold  
**Pre-registration (locked):** https://osf.io/kp5jf (2026-06-19)  
**Target venue:** Nature Cancer / Nature Communications (no wet-lab causal figure)

## Reproduce figures and manuscript

```bash
cd "/Users/stillwell/Documents/Google Drive/Project 51 - Cancer Ne"
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

export MPLCONFIGDIR="$(pwd)/.mpl"
python scripts/run_nat_cancer_figures.py   # figures + rebuilds MANUSCRIPT_draft.docx
```

Or rebuild the Word file alone after figures exist:
```bash
python scripts/build_manuscript_docx.py
```

**Manuscript (DOCX, figures embedded):** `manuscript/MANUSCRIPT_draft.docx`

## Main results (2026-06-19)

| Figure | Finding |
|--------|---------|
| **Fig 2** Cross-cancer (17 types) | r = 0.88, LOO min r = 0.77 — **primary result** |
| **Fig 3** BRAF inhibitor (n=45) | Cox null (P = 0.97) — honest underpowered test |
| **Fig 4** Clinical utility | 2–28% patients ≥ N_e\* by cohort |
| **ED** TCGA PFS | Binary log-rank null (P = 0.55) |

See `docs/STATUS.md` for live status and `docs/MANUSCRIPT_RESULTS_draft.md` for Results prose.

## Layout

```
config/           Locked ε, δ, L, cohorts, Williams N_e anchors
src/              threshold.py, estimators.py, calibration.py, cbioportal.py
scripts/
  make_fig1_clinical.py … make_fig4_utility.py
  make_ed_tcga_null.py
  run_nat_cancer_figures.py
  build_manuscript_docx.py
manuscript/
  MANUSCRIPT_draft.docx
data/fig*/        Generated figures and CSV summaries
docs/
  NAT_CANCER_PLAN.md
  MANUSCRIPT_RESULTS_draft.md
  MANUSCRIPT_ABSTRACT_draft.md
  REPRODUCIBILITY.md
preregistration/
  OSF_deviation_note.md
  OSF_upload_checklist.md
```

## Manuscript

- **Complete draft (DOCX):** `manuscript/MANUSCRIPT_draft.docx` — full Nat Cancer/Comm manuscript with 5 embedded figures
- **Editable source text:** `manuscript/content.py` (rebuild docx after edits)
- **Markdown mirror:** `docs/MANUSCRIPT_full.md`

```bash
python scripts/build_manuscript_docx.py          # Word file
python scripts/export_manuscript_markdown.py   # Markdown export
```

## OSF / GitHub

- Upload steps: `preregistration/OSF_upload_checklist.md`
- Zenodo bundle guide: `docs/REPRODUCIBILITY.md`

## Rules post-registration

Do **not** change ε, δ, L table, or primary cohort list without a new OSF deviation log. Patient N_e calibration is documented in `preregistration/OSF_deviation_note.md`.
