# Cohort matrix — public cBioPortal primary, TRACERx bonus

## Decision record

| Choice | Decision |
|--------|----------|
| Title | A computable threshold below which tumours cannot evolve drug resistance |
| Primary data | cBioPortal public cohorts (no EGA gate for main claim) |
| TRACERx 421 | Bonus validation after primary; EGA EGAS00001006867 |
| Immune / PD-1 | Extended Data only |
| L estimator | Independent driver-locus count — not log₂(N_e) |

---

## Tier 1 — Primary Fig 2 (discovery)

### A. `skcm_broad_brafresist_2012` (mechanistic anchor)

| Field | Value |
|-------|-------|
| n | 46 |
| Drug | Vemurafenib / dabrafenib (BRAF TKI) |
| Endpoint | `DURATION_OF_THERAPY_WEEKS` → months; `EARLY_RESISTANCE` |
| Sequencing | WES; resistance mutations documented |
| L type | SKCM_BRAF (10 loci) |
| Role | Cleanest resistance phenotype; use as Fig 2 inset / mechanistic panel |

**Strength:** Resistance is the endpoint, not OS proxy.  
**Limit:** Small n — combine with TCGA SKCM for power.

### B. TCGA Pan-Cancer Atlas (scale)

| Study | n | Endpoint | L type |
|-------|---|----------|--------|
| `luad_tcga_pan_can_atlas_2018` | 566 | PFS_MONTHS | LUAD_TCGA (18) |
| `skcm_tcga_pan_can_atlas_2018` | 448 | PFS_MONTHS | SKCM_TCGA (10) |
| `coadread_tcga_pan_can_atlas_2018` | 594 | PFS_MONTHS | COADREAD_TCGA (14) |

**Strength:** Harmonized mutation VAFs; consistent N_e / V_A pipeline.  
**Limit:** PFS ≠ pure resistance date — document as pre-specified fallback.

**Pipeline:** Per-patient MATH → V_A; subclonal VAF fraction → h²; VAF SFS → N_e.

---

## Tier 2 — Independent replication

### `prostate_msk_2024`

| Field | Value |
|-------|-------|
| n | 2,260 |
| Therapy | ARSI / metastatic prostate |
| Endpoint | PFS_MONTHS |
| L | PRAD_ARSI (11) |

Distinct disease and institute from TCGA primary — satisfies external replication.

### `nsclc_ctdx_msk_2022` (sensitivity)

| Field | Value |
|-------|-------|
| n | 2,621 |
| Modality | ctDNA |
| Endpoint | OS_MONTHS (sensitivity only) |
| L | NSCLC_general (18) |

Serial ctDNA enables future resistance dating; not primary endpoint.

---

## Tier 3 — Bonus (post-primary)

### TRACERx 421 (EGA EGAS00001006867)

- Per-patient ITH, ctDNA VAF trajectories
- Endpoint: molecular relapse / adaptation rate
- Does **not** gate Nature-family submission if EGA delayed

---

## Excluded

| Study | Reason |
|-------|--------|
| Abbosh 2023 aggregate tertiles | Replaced by patient-level analysis |
| `nsclc_pd1_msk_2018` | ICB; r≈0.15 — Extended Data |
| `tmb_mskcc_2018` | ICB-only |

---

## Endpoint hierarchy (locked)

1. Time to resistance (molecular or clinical progression on first-line targeted agent)
2. PFS (TCGA / MSK with PFS fields)
3. Duration on targeted therapy (BRAF cohort)
4. OS — sensitivity only

---

## Sample size sanity check

| Cohort | Expected events below N_e* | Notes |
|--------|------------------------------|-------|
| TCGA pooled | ~200–400 PFS events | Adequate for KM if ~40% above threshold |
| BRAF resist | ~15 early resistance | Effect-size panel, not standalone |
| MSK prostate | ~800+ PFS events | Strong replication |

---

## Next actions

1. [ ] Register OSF doc (`preregistration/OSF_registration_draft.md`)
2. [ ] Run `scripts/01_inventory_cohorts.py` → `data/cohort_inventory.json`
3. [ ] Wire mutation VAF fetch → replace Fig 2 placeholders
4. [ ] Apply for EGA TRACERx (parallel, non-blocking)
