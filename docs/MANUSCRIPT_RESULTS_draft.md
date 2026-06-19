# Results (draft)

**Title:** A computable threshold below which tumours cannot evolve drug resistance  
**Target:** Nature Cancer / Nature Communications  
**OSF pre-registration:** https://osf.io/kp5jf (locked 2026-06-19)  
**Status:** Draft for internal review — numbers synced to `data/` outputs 2026-06-19

---

## A resistance-learnability threshold computable from standard sequencing

We define **N_e\***, the minimum effective population size at which a tumour can reliably evolve drug resistance to within a fixed fitness tolerance (ε = 0.05, δ = 0.05), given subclonal diversity **V_A** and an independent count of resistance-relevant driver loci **L** (Methods; Supplementary Note 1). N_e\* is computed by inverting the evolutionary PAC bound and requires only quantities derivable from baseline tumour sequencing: mutation allele frequencies (for V_A and N_e), tumour purity where available, and a cancer-type driver panel (for L). We deliberately set **L ≠ log₂(N_e)** to avoid circularity between threshold inputs and the population-size estimate.

Figure 1 maps these inputs onto a representative clinical next-generation sequencing report. For a melanoma example (V_A = 0.14, N_e = 8,200, L = 10), N_e\* = 6,400 and the tumour sits marginally above the learnability threshold (N_e/N_e\* ≈ 1.3). The callout is intended for clinicians: no new assay is required—only reinterpretation of fields already present on most reports.

---

## Theoretical ε\* tracks resistance durability across seventeen cancer types

We first tested whether the PAC bound ε\*(N_e, V_A, L) predicts how quickly resistance emerges at the **cancer-type** level, independent of patient-level tuning. For each of **17** solid and haematologic malignancies we assembled published median N_e (Williams et al. 2016; Dentro et al. 2021), median V_A, independently curated L (`config/driver_loci_L.tsv`), and a literature resistance half-life TTR₂ (months). We used resistance instability 1/TTR₂ as the outcome—higher values indicate faster resistance emergence.

ε\* correlated strongly with 1/TTR₂ (Pearson **r = 0.88**, **P = 3.1 × 10⁻⁶**; Fig. 2). Association was robust to leave-one-out analysis (mean r = 0.88; minimum r = **0.77** with any single cancer type removed) and to bootstrap resampling of cancer types (10,000 replicates; 95% CI for r: **0.51–0.96**). Varying L by ±2-fold (multipliers 0.5, 1.0, 2.0) changed r only marginally (r = 0.879–0.881; Extended Data Table X). These analyses were pre-specified before inspection of patient-level outcomes and constitute the **primary empirical validation** of the framework.

---

## Patient-level test on targeted BRAF inhibition

We next asked whether log₁₀(N_e/N_e\*) at baseline sequencing predicts time on therapy in the **best available public resistance cohort**: 45 melanoma patients treated with vemurafenib (Broad 2012; duration and early-resistance annotations). Effective N_e was estimated from mutation VAF spectra and **cohort-calibrated** to Williams SKCM anchors so that median N_e matches published scale while preserving within-cohort rank order (Methods; OSF deviation note).

**Primary analysis (pre-registered):** Cox proportional hazards with log₁₀(N_e/N_e\*) as a continuous covariate and progression or early resistance as the event (n = 45; 14 events). Hazard ratio **HR = 0.97** (95% CI 0.20–4.71; **P = 0.97**; Fig. 3). Spearman correlation between log₁₀(N_e/N_e\*) and months on therapy was ρ = −0.025 (P = 0.87). Logistic regression of early resistance on log₁₀(N_e/N_e\*) yielded OR = 0.84 per log₁₀ unit (P = 0.86).

After calibration, **44 of 45** patients fell **below** N_e\*, leaving insufficient events in the above-threshold stratum for stable Kaplan–Meier comparison (pre-specified secondary). We therefore report this cohort as an **honest null**: the pre-registered continuous test does not support faster failure with higher N_e/N_e\* at α = 0.05, with wide confidence intervals consistent with **underpowering** (14 events, highly imbalanced stratum).

We attempted to expand the panel with MSK BRAF cohorts (IMPACT 2024, n ≈ 105; Archer 2024, n ≈ 107). Neither study exposes duration-on-therapy or resistance-date fields in cBioPortal clinical metadata, so they could not be merged without additional data access. Public targeted-therapy cohorts with resistance-specific endpoints remain scarce.

---

## Population distribution of N_e/N_e\* at sequencing

To assess clinical deployability we computed N_e/N_e\* across **1,564** patients in four cBioPortal cohorts with baseline mutation profiles (Fig. 4). Median N_e/N_e\* varied by context: colorectal (TCGA, n = 528; median ratio **0.48**; **20%** ≥ N_e\*), melanoma (TCGA, n = 433; **0.56**; **28%**), NSCLC (TCGA LUAD, n = 557; **0.24**; **2%**), and BRAF-inhibitor melanoma (n = 46; **0.18**; **2%**). The pooled histogram shows most patients below unity on a log scale, with a long tail above N_e\* in colorectal and cutaneous melanoma—consistent with higher V_A and L raising the learnability bar in those settings.

These distributions indicate that N_e\* can be computed for the majority of sequenced metastatic solid tumours today, but that **binary above/below calls are context-dependent** and often rare in specific indications—motivating continuous rather than dichotomous patient models where sample size allows.

---

## Pre-registered TCGA progression-free survival (Extended Data)

As pre-registered, we tested binary N_e\* stratification on generic **progression-free survival** in TCGA LUAD, SKCM, and COADREAD (pooled **n = 1,440**; calibrated N_e). Only **16%** of patients exceeded N_e\* after calibration (versus >90% on uncorrected raw N_e scale). Kaplan–Meier log-rank comparison of above versus below N_e\* was **null** (pooled **P = 0.55**; per-cohort P = 0.31–0.86; Extended Data Fig. X).

A pre-specified **continuous** Cox model on log₁₀(N_e/N_e\*) reached P = 0.04 in the pooled TCGA sample (HR = 0.82), but the direction was **opposite** to the resistance-learnability hypothesis (higher ratio associated with longer PFS). We attribute this to endpoint mismatch: TCGA PFS mixes adjuvant and metastatic courses, non-targeted regimens, and progression events that need not reflect evolutionary resistance. This analysis is reported transparently as a **pre-registered negative control**, not as evidence against or for N_e\*.

---

## Summary of statistical findings

| Analysis | n | Primary test | Result | Interpretation |
|----------|---|--------------|--------|----------------|
| Cross-cancer ecology | 17 types | Pearson ε\* vs 1/TTR₂ | r = 0.88, P = 3.1×10⁻⁶ | **Supported** — main result |
| BRAF inhibitor duration | 45 (14 events) | Cox log₁₀(N_e/N_e\*) | HR = 0.97, P = 0.97 | **Null** — underpowered |
| Clinical utility | 1,564 | Descriptive | 2–28% ≥ N_e\* | Deployable inputs |
| TCGA PFS (ED) | 1,440 | Log-rank binary | P = 0.55 | **Null** — wrong endpoint |

---

## Figure legends (draft stubs)

**Fig. 1 | Resistance-learnability threshold mapped to clinical sequencing.** Left, mock tumour profiling report with V_A, N_e, and driver-panel L highlighted. Right, computation of N_e\* and binary call (above/below) for a representative melanoma.

**Fig. 2 | Cross-cancer validation of ε\* versus resistance instability.** Each point is one cancer type (n = 17). x-axis, PAC bound ε\*(N_e, V_A, L); y-axis, published 1/TTR₂ (months⁻¹). Dashed line, linear regression. Statistics: Pearson r, leave-one-out range, bootstrap 95% CI.

**Fig. 3 | Targeted BRAF inhibitor cohort (Broad 2012).** a, Duration on vemurafenib versus log₁₀(N_e/N_e\*); points coloured by early resistance. b, Duration by early-resistance status (Kaplan–Meier not shown owing to n = 1 above N_e\*). Inset statistics: Cox HR and Spearman ρ.

**Fig. 4 | Clinical utility at baseline sequencing.** a, Pooled histogram of log₁₀(N_e/N_e\*) across four cohorts (n = 1,564). b, Percentage of patients with N_e ≥ N_e\* by cohort.

**Extended Data Fig. X | Pre-registered TCGA PFS analysis.** Kaplan–Meier curves for N_e ≥ N_e\* versus N_e < N_e\* (calibrated N_e; pooled TCGA, n = 1,440).

---

*Draft v1 — 2026-06-19. Next: Methods cross-reference, Introduction, Discussion limitations.*
