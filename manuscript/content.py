"""
Full manuscript text for Nature Cancer / Nature Communications submission.
Numbers synced to data/ outputs (2026-06-19).
"""

TITLE = "A computable threshold below which tumours cannot evolve drug resistance"

AUTHORS = "R. Craig Stillwell"

AFFILIATION = "[Affiliation — add department, institution, and country before submission]"

CORRESPONDING = (
    "Correspondence and requests for materials should be addressed to R.C.S. "
    "(craig.stillwell@gmail.com)."
)

GITHUB_REPO = "https://github.com/rstil2/computable-resistance-threshold"

KEYWORDS = (
    "Drug resistance; tumour evolution; effective population size; "
    "intratumour heterogeneity; precision oncology; biomarker"
)

ABSTRACT = [
(
    "Resistance to systemic therapy remains the leading cause of cancer mortality, yet "
    "decisions at diagnosis rarely incorporate a quantitative estimate of whether a tumour "
    "can evolve resistance on the planned regimen. Here we define N_e*, a resistance-learnability "
    "threshold computable from standard tumour sequencing. N_e* depends on three inputs already "
    "reported or derivable from most profiling panels: subclonal diversity (V_A), effective "
    "population size (N_e), and an independently specified count of resistance-relevant driver "
    "loci (L). It marks the minimum heritable population size required for evolution to produce "
    "fit resistant clones within a fixed tolerance (ε = 0.05) with bounded failure probability "
    "(δ = 0.05)."
),
(
    "Across seventeen cancer types, the theoretical PAC bound ε*(N_e, V_A, L) correlates with "
    "published resistance durability (Pearson r = 0.88, P = 3.1 × 10⁻⁶; leave-one-out minimum "
    "r = 0.77), providing pan-cancer ecological validation without patient-level outcome fitting. "
    "In the largest public vemurafenib cohort with resistance-specific annotations (n = 45), "
    "pre-registered association of log(N_e/N_e*) with duration on drug was null (Cox hazard ratio "
    "0.97, P = 0.97), consistent with limited events and calibration placing 44 of 45 patients "
    "below N_e*. Among 1,564 sequenced patients, N_e* was computable from existing report fields; "
    "2–28% exceeded the threshold depending on indication."
),
(
    "N_e* offers a pre-treatment evolutionary risk readout—not a treatment algorithm and not "
    "causal proof of manipulability. Pre-registered generic progression-free survival analyses "
    "were null, highlighting the need for resistance-dated endpoints in prospective validation."
),
]

KEY_POINTS = [
    "N_e* is a resistance-learnability threshold computable from V_A, N_e, and L on standard sequencing reports.",
    "ε* tracks resistance durability across 17 cancer types (r = 0.88), independent of patient-level tuning.",
    "Targeted-therapy patient validation on public data was null but pre-specified; best cohorts lack resistance dates.",
    "Clinical deployment requires no new assay; binary above/below calls are indication-specific and often rare.",
]

INTRODUCTION = [
(
    "Most deaths from advanced cancer follow the emergence of drug-resistant disease. Clinicians "
    "choose regimens using histology, molecular drivers, and staging, but rarely receive a number "
    "that answers a distinct evolutionary question: does this tumour harbour enough heritable "
    "variation, in enough cells, across enough resistance pathways to learn an escape genotype "
    "before control is lost? That question is increasingly addressable because baseline tumour "
    "sequencing—whole-exome, whole-genome, or large targeted panels—already quantifies subclonal "
    "structure through mutation allele frequencies (VAFs), purity estimates, and driver annotations."
),
(
    "Population-genetic theory treats resistance as search on a fitness landscape. Beneficial "
    "alleles must be present or arise in a population large enough to be sampled under selection. "
    "Effective population size N_e summarises that sampling capacity; subclonal diversity V_A "
    "captures how unevenly mutations are distributed across cellular subpopulations; and the "
    "number of independently mutable resistance loci L sets the dimensionality of the search. "
    "Together, these quantities determine whether evolution can approximate an ε-optimal resistant "
    "phenotype with high probability."
),
(
    "We formalise this logic with an evolutionary probably approximately correct (PAC) bound "
    "(Supplementary Note 1). For tolerance ε and failure probability δ, there exists a minimum "
    "N_e*(V_A, L) below which resistance evolution is sample-starved. The bound defines a "
    "computable ε*(N_e, V_A, L) that should covary with resistance emergence rates when inputs "
    "are measured independently of outcomes. A critical design choice is that L is taken from "
    "curated driver panels (OncoKB/CIViC tiered loci) and is not set equal to log₂(N_e), "
    "avoiding circular coupling between threshold inputs and population-size estimates."
),
(
    "We test the framework in three pre-registered settings. First, at the cancer-type level, "
    "does ε* predict published resistance half-lives across diverse malignancies? Second, among "
    "patients receiving BRAF inhibition with resistance-annotated follow-up, does log(N_e/N_e*) "
    "at baseline sequencing predict duration on therapy? Third, in contemporary sequencing cohorts, "
    "what fraction of patients exceed N_e* at diagnosis, and can the required inputs be read from "
    "standard reports? We report pre-registered generic progression-free survival (PFS) analyses "
    "as a negative control where endpoints do not specifically mark evolutionary resistance. We do "
    "not experimentally manipulate N_e; causal tests in barcoded model systems remain separate "
    "future work."
),
]

RESULTS = [
    # Section 1 - before Fig 1
    (
        "heading2",
        "A resistance-learnability threshold from sequencing outputs",
    ),
    (
        "para",
        "N_e* is defined as the smallest effective population size for which the PAC failure "
        "probability is at most δ = 0.05 at accuracy ε = 0.05, given patient-specific V_A and "
        "cancer-type L (Methods; Supplementary Note 1). In practice, V_A is estimated from the "
        "dispersion of mutation VAFs (MATH-score calibration), N_e from the subclonal VAF "
        "site-frequency spectrum (Williams et al. scaling), and L from a fixed panel of "
        "resistance-relevant loci per indication (Extended Data Table 1). All three quantities are "
        "routinely inferable before therapy from a single baseline sequencing sample when purity "
        "is available or estimable."
    ),
    (
        "para",
        "Figure 1 illustrates the clinical mapping. Panel a shows a representative melanoma report "
        "with heterogeneity metrics, effective population size, and driver-panel size highlighted. "
        "Panel b computes N_e* = 9,262 cells for an example with V_A = 0.14, N_e = 8,200, and "
        "L = 10, yielding N_e/N_e* = 0.89 and a below-threshold call. The workflow requires no "
        "proprietary scores beyond locked constants ε and δ; outputs can be appended as an "
        "interpretive line on existing molecular pathology reports."
    ),
    (
        "figure",
        "Figure 1",
        "Resistance-learnability threshold mapped to clinical sequencing. "
        "**a**, Mock tumour profiling summary with inputs V_A, N_e, and L indicated (dashed boxes). "
        "**b**, Computed N_e*, ε*, and patient ratio for representative melanoma (N_e/N_e* = 0.89; "
        "below threshold).",
    ),
    # Section 2 - Fig 2
    (
        "heading2",
        "ε* predicts resistance instability across seventeen cancer types",
    ),
    (
        "para",
        "We assembled independent ecological parameters for seventeen solid and haematologic "
        "malignancies: published median N_e and V_A (Williams et al. 2016; Dentro et al. 2021), "
        "curated L from config/driver_loci_L.tsv, and literature resistance half-life TTR₂ "
        "(Extended Data Table 2). The outcome was resistance instability 1/TTR₂ (months⁻¹); "
        "larger values indicate faster resistance emergence on standard-of-care systemic therapy "
        "for that disease context."
    ),
    (
        "para",
        "ε* correlated strongly with 1/TTR₂ (Pearson r = 0.88, P = 3.1 × 10⁻⁶; Fig. 2). "
        "Fast-resistance leukaemias and glioblastoma occupied the upper envelope (AML, "
        "1/TTR₂ ≈ 0.33 months⁻¹; GBM, 0.25), whereas thyroid cancer and renal cell carcinoma "
        "lay at the lower extreme (THCA, 0.02; KIRC, 0.067). Association was robust to "
        "leave-one-out deletion (mean r = 0.88; minimum r = 0.77 when any single type was "
        "removed) and to bootstrap resampling of cancer types (10,000 replicates; 95% confidence "
        "interval for r: 0.51–0.96). Doubling or halving L changed r by less than 0.002 "
        "(Extended Data Table 3), indicating that the result is not an artefact of a particular "
        "panel size."
    ),
    (
        "para",
        "This analysis was specified before patient-level outcome inspection and provides the "
        "primary empirical support for the framework: a purely sequence-derived evolutionary "
        "quantity tracks cross-cancer resistance ecology without fitting to individual patient "
        "progression times."
    ),
    (
        "figure",
        "Figure 2",
        "Cross-cancer validation of ε* versus resistance instability. "
        "Each point is one cancer type (n = 17). "
        "**x**, PAC bound ε*(N_e, V_A, L); **y**, published 1/TTR₂ (months⁻¹). "
        "Dashed line, ordinary least-squares fit. "
        "Pearson r = 0.88 (P = 3.1 × 10⁻⁶); LOO minimum r = 0.77.",
    ),
    # Section 3 - Fig 3
    (
        "heading2",
        "Pre-registered patient analysis on BRAF inhibition",
    ),
    (
        "para",
        "Patient-level validation used the Broad/Dana-Farber vemurafenib resistance study "
        "(skcm_broad_brafresist_2012), the largest public cohort with baseline exome sequencing "
        "and resistance-focused follow-up (Van Allen et al. 2014). Of 46 enrolled patients, 45 "
        "had usable VAF profiles and annotated duration on vemurafenib; events comprised early "
        "resistance or best response progressive disease (n = 14 events)."
    ),
    (
        "para",
        "Effective N_e was cohort-calibrated to Williams melanoma anchors so median N_e matches "
        "published scale while preserving within-cohort rank order (Methods; OSF deviation note). "
        "The pre-registered primary model was Cox proportional hazards with log₁₀(N_e/N_e*) as a "
        "continuous covariate. The hazard ratio was 0.97 (95% CI 0.20–4.71; P = 0.97; Fig. 3). "
        "Spearman correlation between log₁₀(N_e/N_e*) and months on therapy was ρ = −0.025 "
        "(P = 0.87). Logistic regression of early resistance on log₁₀(N_e/N_e*) gave odds ratio "
        "0.84 per log₁₀ unit (P = 0.86). After calibration, 44 of 45 patients had N_e < N_e*, "
        "leaving a single patient above threshold and preventing stable binary Kaplan–Meier "
        "comparison."
    ),
    (
        "para",
        "We attempted to enlarge the panel with MSK-IMPACT and MSK-Archer BRAF-mutant cohorts "
        "(n ≈ 210 combined). Neither study exposes duration-on-therapy or resistance-date fields "
        "in public cBioPortal metadata, so they could not be merged under pre-registered endpoints. "
        "We therefore interpret the Broad result as an honest null under severe power constraints, "
        "not as definitive evidence against patient-level utility."
    ),
    (
        "figure",
        "Figure 3",
        "Targeted BRAF inhibitor cohort (Broad 2012; n = 45). "
        "**a**, Duration on vemurafenib versus log₁₀(N_e/N_e*); blue, no early resistance; red, early resistance. "
        "**b**, Duration by early-resistance phenotype (box plots). "
        "Cox HR = 0.97 (P = 0.97); Spearman ρ = −0.025.",
    ),
    # Section 4 - Fig 4
    (
        "heading2",
        "Deployability and population-level context",
    ),
    (
        "para",
        "To assess whether N_e* can be computed in contemporary practice, we applied the pipeline "
        "to 1,564 patients across four cBioPortal cohorts with baseline mutation data: TCGA "
        "colorectal (n = 528), cutaneous melanoma (n = 433), LUAD (n = 557), and BRAF-inhibitor "
        "melanoma (n = 46; Fig. 4)."
    ),
    (
        "para",
        "Median N_e/N_e* varied by disease context: colorectal 0.48 (20% of patients ≥ N_e*), "
        "melanoma 0.56 (28%), LUAD 0.24 (2%), and BRAF-treated melanoma 0.18 (2%). The pooled "
        "distribution was skewed below unity on a log scale, with a tail above N_e* in colorectal "
        "and cutaneous melanoma—settings with higher V_A and L that raise the learnability bar. "
        "These patterns imply that binary above/below reporting will often label a minority of "
        "patients in any given clinic, favouring continuous log(N_e/N_e*) where sample size allows."
    ),
    (
        "figure",
        "Figure 4",
        "Clinical utility at baseline sequencing (n = 1,564). "
        "**a**, Pooled histogram of log₁₀(N_e/N_e*); dashed line, N_e = N_e*. "
        "**b**, Percentage of patients with N_e ≥ N_e* by cohort.",
    ),
    # Extended Data
    (
        "heading2",
        "Pre-registered TCGA progression-free survival (negative control)",
    ),
    (
        "para",
        "As pre-registered, we tested N_e* stratification on generic PFS in TCGA LUAD, SKCM, and "
        "COADREAD (pooled n = 1,440 after quality filters). Calibration reduced the fraction "
        "above N_e* from more than 90% on uncorrected raw N_e to 16%, improving stratum balance "
        "(233 above, 1,207 below). Kaplan–Meier log-rank tests were null overall (P = 0.55) and "
        "within each tumour type (COADREAD P = 0.31; LUAD P = 0.86; SKCM P = 0.52; Extended "
        "Data Fig. 1)."
    ),
    (
        "para",
        "A pre-specified continuous Cox model on log₁₀(N_e/N_e*) reached P = 0.04 in the pooled "
        "sample (HR = 0.82), but the direction was opposite to the resistance-learnability "
        "hypothesis (higher ratio associated with longer PFS). We attribute this to endpoint "
        "confounding: TCGA PFS mixes adjuvant and metastatic courses, non-targeted regimens, and "
        "progression that may reflect bulk growth rather than evolutionary escape. We report this "
        "transparently as a negative control rather than as supportive evidence."
    ),
    (
        "figure",
        "Extended Data Fig. 1",
        "Pre-registered TCGA PFS by N_e* stratum (calibrated N_e; pooled n = 1,440). "
        "Red, N_e ≥ N_e* (n = 233); blue, N_e < N_e* (n = 1,207). Log-rank P = 0.55.",
    ),
]

DISCUSSION = [
(
    "This study translates an evolutionary sample-complexity bound into a clinically readable "
    "threshold, N_e*, and tests it at three scales: pan-cancer ecology, targeted-therapy patients, "
    "and population deployability. The central finding is that ε*(N_e, V_A, L)—computed without "
    "reference to individual outcomes—tracks how fast resistance emerges across seventeen cancer "
    "types (r = 0.88). That association survives leave-one-out stress tests and wide variation in "
    "driver-panel size, addressing concerns that the framework merely repackages known heterogeneity "
    "indices."
),
(
    "Patient-level validation on public data did not confirm faster failure with higher "
    "log(N_e/N_e*) in BRAF-mutant melanoma. Interpreting this null requires context. The Broad "
    "cohort offers the cleanest resistance annotations in open data but includes only fourteen "
    "events and, after principled N_e calibration, places ninety-eight percent of patients below "
    "N_e*. MSK BRAF series are larger but lack resistance-dated fields in cBioPortal, illustrating "
    "a broader bottleneck: most genomic archives were built for genotype–outcome association, not "
    "for time-to-resistance on targeted agents. Prospective registries that record molecular "
    "progression dates—and serial ctDNA where available—are the necessary next step."
),
(
    "Deployability is nonetheless immediate in a limited sense. N_e* can be computed from fields "
    "already on sequencing reports, and our distribution analyses show that the threshold is not "
    "trivially exceeded for every patient: the above-threshold fraction ranged from 2% in LUAD and "
    "BRAF-treated melanoma to 28% in TCGA melanoma. Clinicians could receive a continuous "
    "log(N_e/N_e*) readout alongside TMB and driver calls, analogous to how MATH and related scores "
    "summarise heterogeneity—while acknowledging that cut-offs will be indication-specific and "
    "should not drive treatment algorithms without prospective outcome evidence."
),
(
    "Pre-registered TCGA PFS analyses clarify what N_e* is not. Generic PFS is a poor proxy for "
    "evolutionary resistance; the null binary result (P = 0.55) is consistent with endpoint mismatch "
    "rather than biological refutation. The statistically significant but inverted continuous Cox "
    "estimate (HR = 0.82, P = 0.04) further cautions against fishing in all-comer survival endpoints."
),
(
    "Limitations include retrospective design, VAF-based N_e estimation error, post hoc calibration "
    "of N_e to Williams medians (documented on OSF), and literature-derived TTR₂ values for "
    "cross-cancer comparisons. The PAC derivation assumes a simplified fitness landscape; "
    "Supplementary Note 1 provides full theory, but the main text stands on empirics. Causal "
    "manipulation of N_e in barcoded cell systems—holding genetics constant while varying effective "
    "population size—remains the definitive experimental test and was outside scope here."
),
(
    "In summary, N_e* names a resistance-learnability limit computable at diagnosis. Cross-cancer "
    "ecology supports the quantity; patient-level and PFS tests on available public data do not. "
    "The honest package—a strong pan-cancer pattern, transparent nulls, and a clear deployment "
    "path—defines what can be claimed today and what must be proved tomorrow."
),
]

METHODS = [
    ("heading2", "Study design and pre-registration"),
    (
        "para",
        "Analyses were pre-registered on the Open Science Framework (https://osf.io/kp5jf) on "
        "19 June 2026. Fixed constants ε = 0.05, δ = 0.05, the driver-locus table L, primary "
        "cohort identifiers, estimators, and endpoint definitions were locked before inspection "
        "of patient-level results for the reframed submission. A post hoc deviation note documents "
        "cohort-wise calibration of patient N_e to Williams/Dentro median anchors; ε, δ, L, and "
        "cohort lists were unchanged."
    ),
    ("heading2", "PAC bound and N_e*"),
    (
        "para",
        "The evolutionary PAC bound is ε*(N_e, V_A, L) = √(2 V_A [L ln(e N_e/L) + ln(4/δ)] / N_e). "
        "N_e* is the minimum N_e such that the PAC failure probability P(failure) ≤ δ at tolerance ε, "
        "obtained by bisection on the monotone tail (implementation: src/threshold.py). Patient "
        "classification uses baseline sequencing before systemic therapy. The ratio N_e/N_e* is "
        "reported on log₁₀ scale for regression models."
    ),
    ("heading2", "Estimators"),
    (
        "para",
        "V_A: MATH score 100 × MAD(VAF)/median(VAF) from somatic SNV VAFs, scaled to PCAWG "
        "variance units (divide by 180). N_e: subclonal VAF spectrum estimator requiring ≥5 "
        "mutations with 0.05 ≤ VAF ≤ 0.5; cohort-calibrated so median N_e matches "
        "config/williams_Ne_reference.tsv per cancer type while preserving rank order within "
        "cohort. L: integer count from config/driver_loci_L.tsv (OncoKB/CIViC actionable panels, "
        "2024 snapshot); never log₂(N_e). h² proxy (subclonal mutation fraction) is reported in "
        "figures but not used in N_e* inversion. Quality gates: ≥3 mutations; finite V_A and N_e."
    ),
    ("heading2", "Cross-cancer dataset"),
    (
        "para",
        "Seventeen cancer types with published median N_e, V_A, independently assigned L, and "
        "TTR₂ from primary literature (AML: Shlush et al.; GBM: Omuro et al.; SKCM/BRAF: Wagle "
        "et al.; NSCLC-EGFR: Oxnard et al.; NSCLC-ICB: Hellmann et al.; PRAD-met: Scher et al.; "
        "THCA: Haugen et al.; remaining solid tumours: TCGA median or disease-specific reviews; "
        "full table in data/fig2_cross_cancer/cross_cancer_table.csv). Outcome: 1/TTR₂. Statistics: "
        "Pearson correlation; leave-one-out correlation; 10,000 bootstrap replicates resampling "
        "types with replacement; L sensitivity at 0.5×, 1.0×, 2.0× multipliers."
    ),
    ("heading2", "Patient cohorts and endpoints"),
    (
        "para",
        "Mutation and clinical data were retrieved via the cBioPortal public REST API (June 2026). "
        "Targeted therapy: skcm_broad_brafresist_2012 — duration on vemurafenib (weeks converted "
        "to months × 12/52); event if EARLY_RESISTANCE = Yes or TREATMENT_BEST_RESPONSE = PD. "
        "Utility cohorts: luad_tcga_pan_can_atlas_2018, skcm_tcga_pan_can_atlas_2018, "
        "coadread_tcga_pan_can_atlas_2018, skcm_broad_brafresist_2012. Negative control: pooled "
        "TCGA PFS (PFS_MONTHS; event if PFS_STATUS indicates progression). Mutation VAFs cached "
        "locally under data/cache/."
    ),
    ("heading2", "Statistics"),
    (
        "para",
        "Cox proportional hazards (lifelines v0.27) for continuous log₁₀(N_e/N_e*); Kaplan–Meier "
        "and log-rank for binary N_e ≥ N_e* when ≥3 patients per arm; logistic regression for "
        "early resistance. Two-sided α = 0.05. No multiplicity adjustment across secondary "
        "endpoints; pre-registered primary tests are reported verbatim."
    ),
    ("heading2", "Software and reproducibility"),
    (
        "para",
        "Analysis code, locked configuration, and figure scripts are available at "
        f"{GITHUB_REPO} and in the Project 51 working directory. A Zenodo archive "
        "linked to the GitHub release will be published at acceptance."
    ),
]

EXTENDED_DATA_TABLES = [
    (
        "Extended Data Table 1",
        "Inputs to N_e* at baseline sequencing",
        "V_A — subclonal diversity (MATH-calibrated CCF variance proxy). "
        "N_e — effective population size (VAF spectrum estimator, Williams-calibrated). "
        "L — resistance-relevant driver loci (independent panel per cancer type). "
        "ε, δ — fixed at 0.05 (locked pre-registration).",
    ),
    (
        "Extended Data Table 2",
        "Cross-cancer ecological parameters (n = 17 types)",
        "Full numeric values in data/fig2_cross_cancer/cross_cancer_table.csv: "
        "columns Ne, VA, L, ε*, TTR₂, 1/TTR₂ with literature sources per row.",
    ),
    (
        "Extended Data Table 3",
        "Sensitivity of cross-cancer correlation to L panel size",
        "L multiplier 0.5: Pearson r = 0.879 (P = 3.5 × 10⁻⁶). "
        "L multiplier 1.0: r = 0.881 (P = 3.1 × 10⁻⁶). "
        "L multiplier 2.0: r = 0.880 (P = 3.3 × 10⁻⁶).",
    ),
    (
        "Extended Data Table 4",
        "Pre-registered TCGA PFS summary (calibrated N_e)",
        "COADREAD (n = 524): 19.8% above N_e*; log-rank P = 0.31; Cox HR = 0.77 (P = 0.26). "
        "LUAD (n = 497): 1.8% above; log-rank P = 0.86; Cox HR = 0.71 (P = 0.17). "
        "SKCM (n = 419): 28.6% above; log-rank P = 0.52; Cox HR = 0.89 (P = 0.40). "
        "Pooled (n = 1,440): 16.2% above; log-rank P = 0.55; Cox HR = 0.82 (P = 0.042).",
    ),
]

DATA_AVAILABILITY = (
    "Patient-level mutation and clinical data are available through cBioPortal "
    "(https://www.cbioportal.org) under the study accession IDs listed in "
    "config/cohorts.yaml. Processed summary tables and figure statistics are in "
    "data/fig*/. Analysis code and locked parameters: "
    f"{GITHUB_REPO}. Pre-registration: https://osf.io/kp5jf."
)

ETHICS = (
    "This study uses de-identified public retrospective data only; no new human participants "
    "were recruited. Original study ethics approvals are described in the primary publications "
    "for each cBioPortal cohort."
)

ACKNOWLEDGEMENTS = (
    "We thank the cBioPortal and TCGA communities for open access to genomic and clinical data."
)

AUTHOR_CONTRIBUTIONS = (
    "R.C.S. conceived the study, developed the theory, performed all analyses, "
    "generated the figures, and wrote the manuscript."
)

COMPETING_INTERESTS = "The authors declare no competing interests."

REFERENCES = [
    "Williams, M. J. et al. Quantification of subclonal selection in cancer from bulk sequencing data. Nat. Genet. 48, 327–335 (2016).",
    "Dentro, S. C. et al. Characterizing genetic intra-tumor heterogeneity across 2,658 human cancer genomes. Cell 185, 2239–2254 (2022).",
    "Van Allen, E. M. et al. The genetic landscape of clinical resistance to RAF inhibition in metastatic melanoma. Cancer Discov. 4, 94–109 (2014).",
    "Wagle, N. et al. Dissecting therapeutic resistance to RAF inhibition in melanoma by tumor genomic profiling. J. Clin. Oncol. 29, 3085–3096 (2011).",
    "Mroz, E. A. & Rocco, J. W. MATH, a novel measure of intratumor genetic heterogeneity, is high in poor-outcome classes of head and neck squamous cell carcinoma. Oral Oncol. 49, 211–215 (2013).",
    "Cerami, E. et al. The cBio cancer genomics portal: an open platform for exploring multidimensional cancer genomics data. Cancer Discov. 2, 401–404 (2012).",
    "Gao, J. et al. Integrative analysis of complex cancer genomics and clinical profiles using the cBioPortal. Sci. Signal. 6, pl1 (2013).",
    "Shlush, L. I. et al. Tracing the origins of relapse in acute myeloid leukaemia to stem cells. Nature 547, 104–108 (2017).",
    "Omuro, A. & DeAngelis, L. M. Glioblastoma and other malignant gliomas: a clinical review. J. Am. Med. Assoc. 310, 1842–1850 (2013).",
    "Oxnard, G. R. et al. Assessment of resistance mechanisms and clinical implications in patients with EGFR T790M-positive lung cancer and acquired resistance to osimertinib. J. Clin. Oncol. 35, 3482–3488 (2017).",
    "Hellmann, M. D. et al. Nivolumab plus ipilimumab in lung cancer with a high tumor mutational burden. N. Engl. J. Med. 378, 2093–2104 (2018).",
    "Scher, H. I. et al. Increased survival with enzalutamide in prostate cancer after chemotherapy. N. Engl. J. Med. 367, 1187–1197 (2012).",
    "Haugen, B. R. et al. 2015 American Thyroid Association management guidelines for adult patients with thyroid nodules and differentiated thyroid cancer. Thyroid 26, 1–133 (2016).",
    "Osumi, H. et al. Resistance to anti-EGFR antibody in colorectal cancer: mechanisms and strategies. Cancers 13, 981 (2021).",
    "Yates, L. R. et al. Subclonal diversification of primary breast cancer revealed by multiregion sequencing. Nat. Med. 21, 751–759 (2015).",
    "McGranahan, N. & Swanton, C. Clonal heterogeneity and tumor evolution: past, present, and the future. Cell 168, 613–628 (2017).",
    "Greaves, M. & Maley, C. C. Clonal evolution in cancer. Nature 481, 306–313 (2012).",
    "Altrock, P. M., Liu, L. L. & Michor, F. The mathematics of cancer: integrating quantitative models. Nat. Rev. Cancer 15, 730–745 (2015).",
    "Gillies, R. J., Verduzco, D. & Gatenby, R. A. Evolutionary dynamics of carcinogenesis and why targeted therapy does not work. Nat. Rev. Cancer 12, 487–493 (2012).",
    "Davoli, T., Uno, H., Wooten, E. C. & Elledge, S. J. Tumor aneuploidy correlates with markers of immune evasion and with reduced response to immunotherapy. Science 355, eaaf8399 (2017).",
]
