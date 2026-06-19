# OSF Pre-Registration Draft

**Title:** A computable threshold below which tumours cannot evolve drug resistance

**Authors:** R. Craig Stillwell

**Registration date:** 2026-06-19 (timestamped and locked on OSF)

**OSF project link:** https://osf.io/kp5jf

---

## 1. Study information

### 1.1 Research question

Can resistance evolution be predicted at treatment initiation from quantities already in a standard sequencing report — specifically, does each patient’s effective tumour population size \(N_e\) relative to a computable threshold \(N_e^*(V_A, L)\) stratify time-to-drug-resistance?

### 1.2 Hypotheses

**H1 (primary):** Patients with \(N_e \geq N_e^*\) at treatment initiation experience significantly shorter time-to-resistance than patients with \(N_e < N_e^*\) (log-rank \(p < 0.05\)).

**H2 (secondary):** \(\log(N_e / N_e^*)\) is negatively associated with resistance-free survival in a Cox proportional hazards model.

**H3 (cross-cancer):** The theoretical PAC bound \(\varepsilon^*(N_e, V_A, L)\) with **independent** \(L\) correlates with published resistance durability across cancer types (\(r > 0.7\), leave-one-out robust).

### 1.3 Theory framing (demoted)

Evolutionary quantitative genetics and PAC learning share a formal structure (empirical risk minimization on a Fisher-information manifold). This motivates \(N_e^*\) but **is not required** to interpret the empirical results. Full proofs appear in a companion theory manuscript and Supplementary Note 1.

---

## 2. Design

### 2.1 Study type

Retrospective observational validation using publicly available sequencing cohorts (cBioPortal). Prospective TRACERx validation (EGA EGAS00001006867) is **bonus**, not primary.

### 2.2 Primary cohorts (public)

| Priority | Study ID | Disease | Therapy | Endpoint | Expected n |
|----------|----------|---------|---------|----------|------------|
| 1 | `skcm_broad_brafresist_2012` | Melanoma | BRAF inhibitor | Duration on therapy / early resistance | ~46 |
| 2 | `luad_tcga_pan_can_atlas_2018` | NSCLC | Mixed systemic | PFS | ~566 |
| 3 | `skcm_tcga_pan_can_atlas_2018` | Melanoma | Mixed | PFS | ~448 |
| 4 | `coadread_tcga_pan_can_atlas_2018` | CRC | Mixed | PFS | ~594 |

### 2.3 Replication cohorts

| Study ID | Role |
|----------|------|
| `prostate_msk_2024` | Independent disease (ARSI), PFS |
| `nsclc_ctdx_msk_2022` | ctDNA metastatic NSCLC; OS sensitivity only |

### 2.4 Excluded from primary

- `nsclc_pd1_msk_2018` — immune-as-learner (Extended Data only)
- Aggregate TRACERx tertile summaries (Abbosh 2023 Fig 3) — replaced by patient-level data

### 2.5 Bonus

- TRACERx 421 per-patient (EGA) — applied after primary cBioPortal analysis

---

## 3. Variables (fixed before analysis)

### 3.1 Constants

| Symbol | Value | Meaning |
|--------|-------|---------|
| \(\varepsilon\) | 0.05 | Resistance fitness suboptimality tolerance |
| \(\delta\) | 0.05 | PAC failure probability bound |

### 3.2 Per-patient inputs (baseline sequencing only)

| Variable | Estimator | Independence |
|----------|-----------|--------------|
| \(V_A\) | CCF variance across subclones; fallback MATH from VAFs | Not from outcome |
| \(h^2\) | Subclonal mutation fraction (VAF < 0.20) | Not from outcome |
| \(N_e\) | Primary: VAF spectrum (Williams 2016); secondary: purity × burden | Not from outcome |
| \(L\) | Driver/resistance locus count from `driver_loci_L.tsv` (OncoKB panel) | **Never** \(\lfloor \log_2 N_e \rfloor\) |

### 3.3 Threshold

\(N_e^*\) = minimum \(N_e\) such that PAC failure probability \(\leq \delta\), computed by numerical inversion (`threshold.ne_star`).

**Stratification:** Binary at \(N_e \geq N_e^*\) vs \(N_e < N_e^*\).

### 3.4 Primary endpoint

**Time to resistance** (months): first molecular resistance, RECIST progression on first-line agent, or switch to second line for progression.

**Fallback (pre-specified):** PFS where resistance date unavailable; duration-on-therapy for BRAF cohort.

---

## 4. Analysis plan

### 4.1 Primary analysis

1. Compute \(N_e\), \(V_A\), \(L\), \(N_e^*\) for each eligible patient at baseline.
2. Kaplan–Meier resistance-free survival stratified above vs below \(N_e^*\).
3. Log-rank test; report HR with 95% CI from Cox model.
4. Pool TCGA cohorts with random patient-level meta-analysis if heterogeneity I² < 50%; otherwise report per-cohort forest plot.

### 4.2 Secondary / sensitivity

- Cox with continuous \(\log(N_e / N_e^*)\)
- Secondary \(N_e\) estimator (cellularity)
- Landmark analysis at 3 months (ctDNA cohorts)
- OS instead of PFS (`nsclc_ctdx_msk_2022` only)

### 4.3 Fig 3 cross-cancer

- \(\varepsilon^*\) with independent \(L\) from driver table
- Leave-one-cancer-out Pearson \(r\)
- 10,000 bootstrap CIs
- \(L\) sensitivity: 0.5×, 1×, 2× cancer-type counts

### 4.4 Multiplicity

Primary hypothesis H1 controls family-wise error at \(\alpha = 0.05\) for the pooled primary KM. Secondary analyses are exploratory unless noted.

---

## 5. Deviations log

| Date | Deviation | Rationale |
|------|-----------|-----------|
| | | |

---

## 6. Data and code

- **Repository:** `github.com/rstil2/selection-as-learning` (branch: `clinical-paper`)
- **Config:** `clinical_paper/config/fixed_parameters.yaml`
- **Registration lock:** Commit hash [TO RECORD AT REGISTRATION]

---

## 7. Future experimental work (not part of this registration)

- **Fig 4:** Barcoded cell-line evolution with manipulated bottleneck size (causal)
- **Fig 5:** Organoid/PDX combination vs sequential at matched cytotoxicity
- **Clinical capstone:** Prospective cohort with pre-registered \(N_e^*\) at diagnosis
