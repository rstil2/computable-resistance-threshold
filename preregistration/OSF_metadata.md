# OSF metadata — copy-paste for project setup

Use this file when filling out the OSF project page and the preregistration registration form.

**OSF project:** https://osf.io/kp5jf

---

## OSF project (top level)

**Project title**
```
A computable threshold below which tumours cannot evolve drug resistance
```

**Project description** (paste into OSF “Description” field)
```
Pre-registration and analysis materials for a clinical oncology study testing whether drug resistance evolution can be predicted at treatment initiation from standard sequencing outputs.

We define a patient-specific resistance-learnability threshold N_e* — computed from intratumour heterogeneity (V_A / h² proxies) and effective tumour population size (N_e) — and test whether patients above vs. below this threshold differ in time-to-resistance. Primary validation uses public cBioPortal cohorts (TCGA Pan-Cancer Atlas, BRAF-inhibitor resistance cohort); independent replication uses MSK metastatic cohorts. TRACERx per-patient data (EGA) is planned as bonus validation.

This OSF project locks the analysis plan, fixed parameters (ε, δ, independent L estimator), cohort list, and endpoints before outcome-unblinded analysis. Companion theory work is published separately; this registration covers the empirical clinical validation only.

Author: R. Craig Stillwell, University of Kentucky
```

**Tags / keywords**
```
cancer, drug resistance, effective population size, intratumour heterogeneity, evolutionary oncology, pre-registration, cBioPortal, TCGA, sample complexity
```

**License (project)**
```
CC-BY 4.0
```
(or your preference — CC0 if you want maximum reuse of preregistration text)

**Affiliation**
```
University of Kentucky
```

---

## Preregistration registration (nested under project)

**Registration title**
```
Pre-analysis plan: N_e* threshold and time-to-resistance in public sequencing cohorts
```

**Description / abstract** (registration summary field)
```
Research question: Does each patient’s effective tumour population size N_e, relative to a computable threshold N_e*(V_A, L) at treatment initiation, stratify time-to-drug-resistance?

Primary hypothesis (H1): Patients with N_e ≥ N_e* experience significantly shorter time-to-resistance than patients with N_e < N_e* (log-rank p < 0.05).

Design: Retrospective observational validation in public cBioPortal cohorts. Primary cohorts: skcm_broad_brafresist_2012 (BRAF TKI), luad/skcm/coadread TCGA Pan-Cancer Atlas (PFS). Replication: prostate_msk_2024; sensitivity: nsclc_ctdx_msk_2022 (OS). TRACERx 421 (EGA EGAS00001006867) is bonus, not primary.

Threshold inputs fixed before analysis: V_A from CCF variance or MATH score; h² from subclonal mutation fraction; N_e from VAF site-frequency spectrum; L from independent driver-locus panel (not log2 N_e). Constants: ε = 0.05, δ = 0.05.

Full analysis plan: see OSF_registration_draft.md in this project.
```

**Study type**
```
Registration / Pre-registration
```

**Subjects**
```
Humans — retrospective cancer genomics cohorts (de-identified public data)
```

**Hypotheses** (short list for form)
```
H1: N_e ≥ N_e* → shorter time-to-resistance (log-rank p < 0.05)
H2: log(N_e/N_e*) negatively associated with resistance-free survival (Cox)
H3: ε*(N_e, V_A, L) correlates with cross-cancer resistance durability (r > 0.7, LOO robust)
```

**Design**
```
Retrospective cohort study; no new data collection for primary analysis
```

**Primary endpoint**
```
Time to resistance (months): molecular resistance, RECIST progression on first-line therapy, or switch to second line for progression. Fallback: PFS (TCGA/MSK) or duration on targeted therapy (BRAF cohort).
```

**Secondary endpoints**
```
Cox model with continuous log(N_e/N_e*); cross-cancer ε* correlation with independent L; landmark analysis at 3 months; OS sensitivity in ctDNA cohort
```

**Sample size**
```
Primary: ~1,600+ patients across cBioPortal TCGA cohorts + 46 BRAF-resistance patients. Replication: ~2,260 MSK prostate.
```

**Blinding**
```
Not applicable — retrospective analysis of public data; analysis plan registered before primary outcome modeling with final VAF pipeline
```

---

## What to upload to OSF

| File | Purpose |
|------|---------|
| `preregistration/OSF_registration_draft.md` | Full pre-analysis plan (main registration document) |
| `config/fixed_parameters.yaml` | Locked ε, δ, endpoints, estimator rules |
| `config/driver_loci_L.tsv` | Independent L values |
| `config/cohorts.yaml` | Cohort inclusion/exclusion |

Optional after registration lock:
- Git commit hash or Zenodo DOI once code is archived

---

## Fields you can leave blank or use defaults

| OSF field | Suggestion |
|-----------|------------|
| Funding | None / self-funded (unless you have a grant) |
| DOI | Assign after upload (OSF will generate) |
| Related projects | Link companion theory preprint when available |
| Data availability | “All primary data from cBioPortal public API; see cohorts.yaml” |
| Ethics | Exempt — secondary analysis of de-identified public data (confirm with your IRB if needed) |

---

## Sampling strategy and data collection (OSF form field)

**Paste into:** “Describe the process by which you will define your sampling strategy and collect new data…”

```
No new primary data will be collected. This is a retrospective observational study using existing, de-identified public cancer genomics cohorts. Data will be gathered programmatically from the cBioPortal for Cancer Genomics public REST API (https://www.cbioportal.org/api) and prepared with a single harmonized per-patient pipeline (mutation VAFs → V_A, h², N_e; clinical fields → time-to-resistance endpoints).

Population: Adults with solid tumours who received systemic therapy and have baseline tumour sequencing (WES/WGS or targeted panel) with linked clinical outcome data.

Sampling frame: All patients in pre-specified public cBioPortal study IDs listed in config/cohorts.yaml (uploaded to this registration). Primary discovery cohorts: skcm_broad_brafresist_2012 (melanoma, BRAF inhibitor; n≈46), luad_tcga_pan_can_atlas_2018 (NSCLC; n≈566), skcm_tcga_pan_can_atlas_2018 (melanoma; n≈448), coadread_tcga_pan_can_atlas_2018 (colorectal; n≈594). Independent replication: prostate_msk_2024 (metastatic prostate, ARSI; n≈2,260). Sensitivity only: nsclc_ctdx_msk_2022 (metastatic NSCLC ctDNA; OS endpoint). Bonus validation (not primary): TRACERx 421 per-patient data via EGA accession EGAS00001006867, applied after cBioPortal analysis.

Recruitment: Not applicable — patients were enrolled in source studies by original investigators. We include all eligible patients meeting criteria below within each study ID.

Inclusion criteria (all cohorts): (1) patient appears in the pre-specified cBioPortal study; (2) baseline or pre-treatment sequencing sample with mutation-level VAF data available; (3) non-missing primary or fallback outcome (time-to-resistance, PFS, or duration on targeted therapy per cohort-specific rules in fixed_parameters.yaml); (4) sufficient mutations to estimate V_A and N_e (≥5 subclonal VAFs in [0.05, 0.5] for N_e SFS estimator).

Exclusion criteria: (1) studies excluded a priori (nsclc_pd1_msk_2018, tmb_mskcc_2018 — immunotherapy-only, not targeted resistance); (2) patients missing both primary and pre-specified fallback endpoints; (3) samples with no usable mutation VAF data; (4) pancreatic adenocarcinoma in cross-cancer Fig 3 analysis only (stromal confound, pre-specified).

Source/location: cBioPortal-hosted TCGA Pan-Cancer Atlas and MSK/Broad published cohorts (USA/international TCGA sites). Cached clinical tables stored locally under data/cache/ with study ID and fetch date recorded. Full cohort list and endpoint mappings: config/cohorts.yaml and config/fixed_parameters.yaml (uploaded).

Data preparation: For each eligible patient, compute N_e*, V_A, L, and N_e at the baseline sequencing timepoint only, using estimators defined in fixed_parameters.yaml and L values from driver_loci_L.tsv (independent of N_e). Outcome data will not be used to define inputs. Analysis code: scripts/01_inventory_cohorts.py, scripts/03_fig2_km_analysis.py.

Expected duration: Data download and cohort assembly from cBioPortal, June 2025–June 2026. Primary outcome modeling begins only after this registration is timestamped. TRACERx EGA access (if approved) is a post-primary add-on with no change to locked parameters.

Full detail: OSF_registration_draft.md (Section 2), config/cohorts.yaml, config/fixed_parameters.yaml.
```

---

## After you create the project

1. Paste the OSF project URL into `OSF_registration_draft.md` (line 9).
2. Upload the four files listed above.
3. Note registration timestamp and add to `config/fixed_parameters.yaml` under a new `osf:` key.
4. Do not change ε, δ, L table, or cohort list after registration.
