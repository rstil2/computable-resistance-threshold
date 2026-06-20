"""
Full manuscript text — Nature Cancer / Nature Communications.
Numbers verified against data/ outputs (2026-06-19).
Repository: https://github.com/rstil2/computable-resistance-threshold
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
    "Resistance to systemic therapy drives most cancer deaths, yet treatment decisions at "
    "diagnosis seldom include a quantitative estimate of evolutionary capacity to escape therapy. "
    "We define N_e*, a resistance-learnability threshold computable from standard tumour "
    "sequencing: subclonal diversity (V_A), effective population size (N_e), and an independently "
    "specified count of resistance-relevant driver loci (L). Under a fixed evolutionary tolerance "
    "(ε = 0.05) and failure probability (δ = 0.05), N_e* is the minimum population size at which "
    "resistance evolution is reliably learnable in the PAC sense (Supplementary Note 1)."
),
(
    "Across seventeen cancer types, the bound ε*(N_e, V_A, L) correlates with published "
    "resistance durability (Pearson r = 0.88, P = 3.1 × 10⁻⁶; leave-one-out minimum r = 0.77), "
    "validating pan-cancer resistance ecology without patient-level outcome fitting. In the largest "
    "public vemurafenib cohort with resistance-specific annotations (n = 45), pre-registered "
    "association of log(N_e/N_e*) with duration on drug was null (Cox hazard ratio 0.97, 95% CI "
    "0.20–4.71, P = 0.97), consistent with fourteen events and 44 of 45 patients below N_e* after "
    "calibration. Among 1,564 sequenced patients, all inputs were available from existing report "
    "fields; 2–28% exceeded N_e* depending on indication."
),
(
    "N_e* is a pre-treatment evolutionary risk readout, not a treatment algorithm or proof that "
    "N_e is causally manipulable. Pre-registered generic progression-free survival analyses were "
    "null (log-rank P = 0.55), underscoring the need for resistance-dated endpoints in "
    "prospective validation."
),
]

KEY_POINTS = [
    "N_e* quantifies resistance learnability from V_A, N_e, and L already present on most sequencing reports.",
    "ε* tracks resistance durability across 17 cancer types (r = 0.88), with no patient-level tuning.",
    "Public targeted-therapy cohorts yield a pre-specified null patient test; resistance-dated endpoints are scarce.",
    "Binary above/below calls are indication-specific and often rare; continuous log(N_e/N_e*) is preferred.",
]

INTRODUCTION = [
(
    "Advanced cancer kills most often when tumours evolve drug resistance. Oncologists select "
    "regimens from histology, driver mutations, and stage, but a separate question usually goes "
    "unquantified: does this tumour contain enough heritable variation, in enough cells, across "
    "enough resistance pathways to discover an escape genotype before the current therapy fails? "
    "Baseline tumour sequencing—exome, genome, or large targeted panel—already contains the "
    "information needed to approach that question through mutation allele frequencies (VAFs), "
    "purity estimates, and driver annotations."
),
(
    "From a population-genetic perspective, resistance is search on a fitness landscape under "
    "selection. Beneficial alleles must be present or arise in a population large enough to be "
    "sampled before sensitive clones are eliminated. Effective population size N_e governs that "
    "sampling capacity; subclonal diversity V_A describes how unevenly mutations partition across "
    "cellular subpopulations; and the number of independently mutable resistance loci L defines "
    "search dimensionality. Together they determine whether evolution can approximate an "
    "ε-optimal resistant phenotype with bounded error."
),
(
    "We cast this logic as an evolutionary probably approximately correct (PAC) bound "
    "(Supplementary Note 1). For fixed ε and δ there exists a minimum N_e*(V_A, L) below which "
    "resistance evolution is sample-starved. The bound yields ε*(N_e, V_A, L), which should "
    "covary with resistance emergence when its inputs are measured independently of clinical "
    "outcome. Importantly, L is fixed from curated OncoKB/CIViC resistance panels and is not "
    "derived from log₂(N_e), avoiding circular coupling between the threshold and the population "
    "size estimate."
),
(
    "We test three pre-registered predictions. First, ε* should track published resistance "
    "half-lives across cancer types. Second, among vemurafenib-treated melanoma patients with "
    "resistance-annotated follow-up, log(N_e/N_e*) at baseline should predict duration on drug. "
    "Third, N_e* should be computable from standard sequencing reports, with a measurable "
    "fraction of patients above threshold at diagnosis. Generic TCGA progression-free survival "
    "(PFS) serves as a pre-specified negative control when endpoints do not mark evolutionary "
    "resistance. We do not experimentally manipulate N_e; causal tests in barcoded model systems "
    "are deferred."
),
]

RESULTS = [
    (
        "heading2",
        "A resistance-learnability threshold from sequencing outputs",
    ),
    (
        "para",
        "N_e* is the smallest effective population size for which the PAC failure probability "
        "does not exceed δ = 0.05 at accuracy ε = 0.05, given patient V_A and cancer-type L "
        "(Methods; Supplementary Note 1). V_A is estimated from VAF dispersion (MATH-score "
        "calibration), N_e from the subclonal VAF site-frequency spectrum (Williams et al. "
        "scaling), and L from a fixed resistance-locus panel per indication (Extended Data "
        "Table 1). Each quantity is inferable from a single pre-treatment sample when tumour "
        "purity is known or estimable."
    ),
    (
        "para",
        "Figure 1 maps the computation onto a representative melanoma report. Panel a highlights "
        "heterogeneity, effective population size, and driver-panel size—the three inputs already "
        "present on most molecular pathology summaries. Panel b computes N_e* = 9,262 cells for "
        "V_A = 0.14, N_e = 8,200, and L = 10, giving N_e/N_e* = 0.89 and a below-threshold "
        "call in the PAC sense. No proprietary assay is required; the output can be appended as "
        "an interpretive line on existing reports."
    ),
    (
        "figure",
        "Figure 1",
        "Resistance-learnability threshold mapped to clinical sequencing. "
        "a, Mock tumour profiling summary with inputs V_A, N_e, and L (dashed boxes). "
        "b, Computed N_e*, ε*, and patient ratio (N_e/N_e* = 0.89; below threshold).",
    ),
    (
        "heading2",
        "ε* predicts resistance instability across seventeen cancer types",
    ),
    (
        "para",
        "We compiled independent ecological parameters for seventeen malignancies: published "
        "median N_e and V_A (Williams et al. 2016; Dentro et al. 2021), curated L, and literature "
        "resistance half-life TTR₂ (Extended Data Table 2). The outcome was resistance instability "
        "1/TTR₂ (months⁻¹), with larger values indicating faster resistance on standard systemic "
        "therapy in each disease context."
    ),
    (
        "para",
        "ε* correlated strongly with 1/TTR₂ (Pearson r = 0.88, P = 3.1 × 10⁻⁶; Fig. 2). "
        "Acute myeloid leukaemia and glioblastoma occupied the fast-resistance extreme (1/TTR₂ ≈ "
        "0.33 and 0.25 months⁻¹, respectively); thyroid carcinoma and renal cell carcinoma lay "
        "at the slow extreme (0.02 and 0.067). Leave-one-out deletion left the association intact "
        "(mean r = 0.88; minimum r = 0.77). Bootstrap resampling of cancer types (10,000 "
        "replicates) gave a 95% confidence interval for r of 0.51–0.96, reflecting uncertainty "
        "from the modest number of types rather than fragility of the estimate. Halving or "
        "doubling L changed r by at most 0.002 (Extended Data Table 3)."
    ),
    (
        "para",
        "Specified before inspection of patient outcomes, this analysis is the primary empirical "
        "support for the framework: a sequence-derived evolutionary quantity tracks cross-cancer "
        "resistance ecology without regression to individual progression times."
    ),
    (
        "figure",
        "Figure 2",
        "Cross-cancer validation of ε* versus resistance instability (n = 17 types). "
        "x-axis, PAC bound ε*(N_e, V_A, L); y-axis, published 1/TTR₂ (months⁻¹). "
        "Dashed line, OLS fit. Pearson r = 0.88 (P = 3.1 × 10⁻⁶); LOO minimum r = 0.77.",
    ),
    (
        "heading2",
        "Pre-registered patient analysis on BRAF inhibition",
    ),
    (
        "para",
        "Patient-level validation used the Broad/Dana-Farber vemurafenib cohort "
        "(skcm_broad_brafresist_2012; Van Allen et al. 2014)—the largest public dataset with "
        "baseline exome sequencing and resistance-focused follow-up. Forty-five of forty-six "
        "patients had usable VAF profiles and duration on vemurafenib; the pre-registered event "
        "combined early resistance annotation or best response progressive disease (fourteen "
        "events)."
    ),
    (
        "para",
        "Patient N_e was cohort-calibrated to Williams melanoma anchors, preserving rank order "
        "within the study (Methods; OSF deviation note). The pre-registered primary model was Cox "
        "regression with log₁₀(N_e/N_e*) as a continuous covariate. Hazard ratio 0.97 (95% CI "
        "0.20–4.71; P = 0.97; Fig. 3). Spearman ρ between log₁₀(N_e/N_e*) and months on therapy "
        "was −0.025 (P = 0.87). Logistic regression of early resistance on log₁₀(N_e/N_e*) gave "
        "odds ratio 0.84 per log₁₀ unit (P = 0.86). Forty-four of forty-five patients had "
        "N_e < N_e*, leaving one above threshold and precluding stable binary Kaplan–Meier "
        "comparison."
    ),
    (
        "para",
        "We sought to expand the panel with MSK-IMPACT and MSK-Archer BRAF-mutant cohorts "
        "(≈210 patients combined). Neither exposes duration-on-therapy or resistance-date fields "
        "in public cBioPortal metadata, so they could not be merged under pre-registered endpoints. "
        "We report the Broad result as a pre-specified null under severe power constraints—not as "
        "evidence against patient-level utility in better-annotated cohorts."
    ),
    (
        "figure",
        "Figure 3",
        "Targeted BRAF inhibitor cohort (Broad 2012; n = 45). "
        "a, Duration on vemurafenib versus log₁₀(N_e/N_e*); blue, no early resistance; red, early resistance. "
        "b, Duration by early-resistance phenotype. Cox HR = 0.97 (P = 0.97).",
    ),
    (
        "heading2",
        "Population distribution and clinical deployability",
    ),
    (
        "para",
        "We applied the pipeline to 1,564 patients in four cBioPortal cohorts with baseline "
        "mutation data: TCGA colorectal (n = 528), cutaneous melanoma (n = 433), LUAD (n = 557), "
        "and BRAF-inhibitor melanoma (n = 46; Fig. 4). Every patient passed genomic quality "
        "filters and yielded finite V_A and N_e."
    ),
    (
        "para",
        "Median N_e/N_e* varied by context: colorectal 0.48 (20% ≥ N_e*), melanoma 0.56 (28%), "
        "LUAD 0.24 (2%), BRAF-treated melanoma 0.18 (2%). The pooled distribution skewed below "
        "unity on a log scale, with an upper tail in colorectal and cutaneous melanoma—settings "
        "where higher V_A and L raise the learnability bar. Binary above/below reporting will "
        "therefore label a minority in many clinics; continuous log(N_e/N_e*) is the appropriate "
        "default for statistical modelling."
    ),
    (
        "figure",
        "Figure 4",
        "Clinical utility at baseline sequencing (n = 1,564). "
        "a, Pooled histogram of log₁₀(N_e/N_e*); dashed line, N_e = N_e*. "
        "b, Percentage with N_e ≥ N_e* by cohort.",
    ),
    (
        "heading2",
        "Pre-registered TCGA PFS as negative control",
    ),
    (
        "para",
        "Pre-registered binary stratification on generic PFS in TCGA LUAD, SKCM, and COADREAD "
        "yielded pooled n = 1,440 after quality filters. Calibration reduced the fraction above "
        "N_e* from >90% on uncorrected N_e to 16.2% (233 above, 1,207 below). Kaplan–Meier "
        "log-rank tests were null overall (P = 0.55) and within each type (COADREAD P = 0.31; "
        "LUAD P = 0.86; SKCM P = 0.52; Extended Data Fig. 1; Extended Data Table 4)."
    ),
    (
        "para",
        "Continuous Cox regression on log₁₀(N_e/N_e*) in the pooled sample reached P = 0.042 "
        "(HR = 0.82)—significant but opposite to the pre-registered direction (higher ratio "
        "associated with longer PFS). TCGA PFS conflates adjuvant and metastatic disease, mixed "
        "regimens, and progression that need not reflect evolutionary escape. We treat this as a "
        "negative control illustrating endpoint mismatch, not as supportive or refuting evidence."
    ),
    (
        "figure",
        "Extended Data Fig. 1",
        "Pre-registered TCGA PFS by N_e* stratum (n = 1,440). "
        "Red, N_e ≥ N_e* (n = 233); blue, N_e < N_e* (n = 1,207). Log-rank P = 0.55.",
    ),
]

DISCUSSION = [
(
    "We translate an evolutionary sample-complexity bound into N_e*, a threshold readable on "
    "standard sequencing reports, and test it at three scales. The principal finding is ecological: "
    "ε*(N_e, V_A, L), computed without reference to patient outcomes, tracks how quickly "
    "resistance emerges across seventeen cancer types (r = 0.88). That result survives "
    "leave-one-out deletion and wide perturbation of L, and does not reduce to repackaging "
    "existing heterogeneity indices because L is fixed independently of N_e."
),
(
    "The title’s claim—that resistance cannot evolve below N_e*—is intended in the PAC sense "
    "of reliable learnability under bounded error, not as a guarantee that no resistant clone "
    "will ever appear. Empirically, patient-level and PFS tests on public data neither confirm "
    "nor refute that stronger reading; they were underpowered or used mismatched endpoints. The "
    "Broad vemurafenib cohort (fourteen events; 98% below N_e* after calibration) cannot "
    "discriminate subtle hazard differences. Larger MSK BRAF series exist but lack resistance "
    "dates in open metadata—a systematic gap in genomic archives built for genotype–survival "
    "association rather than time-to-resistance on targeted agents."
),
(
    "Deployability is more immediate. All inputs for N_e* are already reported or derivable on "
    "most panels, and only 2–28% of patients exceeded the threshold in our distribution analysis, "
    "depending on indication. A continuous log(N_e/N_e*) line item—alongside TMB and driver "
    "calls—could frame evolutionary risk without implying that a binary cut should alter "
    "treatment until prospective outcome evidence exists."
),
(
    "Pre-registered TCGA PFS analyses delimit what not to claim. Generic PFS is a poor proxy for "
    "resistance evolution; the null binary result (P = 0.55) is exactly what endpoint mismatch "
    "predicts. The significant inverted continuous Cox estimate (HR = 0.82, P = 0.042) warns "
    "against exploratory survival mining without resistance-specific labels."
),
(
    "Limitations include retrospective design, error in VAF-based N_e estimation, post hoc "
    "calibration of N_e to Williams medians (documented on OSF), and literature-derived TTR₂ "
    "for cross-cancer comparisons. The PAC landscape is simplified; full derivations appear in "
    "Supplementary Note 1. Definitive causal proof requires experimental control of effective "
    "population size—outside the scope of this observational study."
),
(
    "N_e* names a computable resistance-learnability limit at diagnosis. Cross-cancer ecology "
    "supports it; available patient-level tests do not. Presenting both—with a clear deployment "
    "path and transparent nulls—states honestly what sequencing can say about evolutionary risk "
    "today."
),
]

METHODS = [
    ("heading2", "Study design and pre-registration"),
    (
        "para",
        "Hypotheses, estimators, constants (ε = 0.05, δ = 0.05), driver-locus table L, cohort "
        "identifiers, and endpoint definitions were registered on the Open Science Framework "
        "(https://osf.io/kp5jf) on 19 June 2026 before inspection of patient-level results for "
        "this reframed analysis. A documented deviation added cohort-wise calibration of patient "
        "N_e to Williams/Dentro median anchors; ε, δ, L, and cohort lists were unchanged."
    ),
    ("heading2", "PAC bound and N_e*"),
    (
        "para",
        "The bound ε*(N_e, V_A, L) = √(2 V_A [L ln(e N_e/L) + ln(4/δ)] / N_e). N_e* solves "
        "P(failure) ≤ δ at tolerance ε by bisection on the monotone PAC tail. Classification "
        "uses baseline sequencing before systemic therapy. Regression models employ log₁₀(N_e/N_e*)."
    ),
    ("heading2", "Estimators"),
    (
        "para",
        "V_A: MATH score (100 × MAD(VAF)/median(VAF)) scaled to PCAWG variance units (/180). "
        "N_e: subclonal VAF spectrum estimator (≥5 mutations with 0.05 ≤ VAF ≤ 0.5), "
        "cohort-calibrated to published median N_e per cancer type while preserving within-cohort "
        "rank order. L: integer resistance-locus count from a fixed OncoKB/CIViC panel snapshot "
        "(June 2024); never log₂(N_e). Subclonal mutation fraction (h² proxy) appears in Fig. 1 "
        "for clinical context but does not enter N_e* inversion. Quality gates: ≥3 mutations; "
        "finite V_A and N_e."
    ),
    ("heading2", "Cross-cancer dataset"),
    (
        "para",
        "Seventeen cancer types with published median N_e, V_A, independently assigned L, and "
        "TTR₂ (sources in Supplementary Table 1 and repository file "
        "cross_cancer_table.csv). Outcome: 1/TTR₂. Statistics: Pearson r; leave-one-out r; "
        "10,000 bootstrap replicates resampling types; L sensitivity at 0.5×, 1.0×, 2.0×."
    ),
    ("heading2", "Patient cohorts and endpoints"),
    (
        "para",
        "Mutation and clinical data were retrieved from the cBioPortal REST API (June 2026). "
        "Targeted therapy: skcm_broad_brafresist_2012 — duration on vemurafenib (weeks × 12/52 "
        "= months); event if early resistance or best response PD. Utility: TCGA LUAD, SKCM, "
        "COADREAD, and the Broad BRAF cohort. Negative control: pooled TCGA PFS (progression on "
        "PFS_STATUS). VAF data are downloaded on first pipeline run and cached locally."
    ),
    ("heading2", "Statistics"),
    (
        "para",
        "Cox proportional hazards (lifelines 0.27) for continuous log₁₀(N_e/N_e*); Kaplan–Meier "
        "and log-rank for binary N_e ≥ N_e* when ≥3 patients per arm; logistic regression for "
        "early resistance. Two-sided α = 0.05. Pre-registered primary tests are reported "
        "without multiplicity adjustment; secondary and negative-control analyses are labelled "
        "explicitly."
    ),
    ("heading2", "Software and reproducibility"),
    (
        "para",
        f"Analysis code, locked configuration, and figure scripts: {GITHUB_REPO}. "
        "Regenerate all outputs: python scripts/run_nat_cancer_figures.py. A Zenodo archive "
        "linked to the GitHub release will be minted at acceptance."
    ),
]

EXTENDED_DATA_TABLES = [
    (
        "Extended Data Table 1",
        "Inputs to N_e* at baseline sequencing",
        "V_A — subclonal diversity (MATH-calibrated variance proxy). "
        "N_e — effective population size (VAF spectrum, Williams-calibrated). "
        "L — resistance-relevant driver loci (independent panel). ε, δ — 0.05 (pre-registered).",
    ),
    (
        "Extended Data Table 2",
        "Cross-cancer ecological parameters (n = 17)",
        "Full Ne, V_A, L, ε*, TTR₂, and 1/TTR₂ with literature sources — see Supplementary "
        "Table 1 and cross_cancer_table.csv in the code repository.",
    ),
    (
        "Extended Data Table 3",
        "Sensitivity of cross-cancer correlation to L",
        "L × 0.5: r = 0.879 (P = 3.5 × 10⁻⁶). L × 1.0: r = 0.881 (P = 3.1 × 10⁻⁶). "
        "L × 2.0: r = 0.880 (P = 3.3 × 10⁻⁶).",
    ),
    (
        "Extended Data Table 4",
        "Pre-registered TCGA PFS (calibrated N_e)",
        "COADREAD (n = 524): 19.8% above N_e*; log-rank P = 0.31; Cox HR = 0.77 (P = 0.26). "
        "LUAD (n = 497): 1.8%; log-rank P = 0.86; HR = 0.71 (P = 0.17). "
        "SKCM (n = 419): 28.6%; log-rank P = 0.52; HR = 0.89 (P = 0.40). "
        "Pooled (n = 1,440): 16.2%; log-rank P = 0.55; HR = 0.82 (P = 0.042).",
    ),
]

DATA_AVAILABILITY = (
    "Patient-level data are available through cBioPortal (https://www.cbioportal.org) under study "
    "accessions listed in the repository cohort manifest. Processed figure statistics and patient "
    f"summary tables accompany the code release at {GITHUB_REPO}. Pre-registration: "
    "https://osf.io/kp5jf."
)

ETHICS = (
    "De-identified retrospective public data only; no new human participants. Ethics approvals "
    "for original cohorts are described in their primary publications."
)

ACKNOWLEDGEMENTS = (
    "The author thanks the cBioPortal and TCGA communities for open genomic and clinical data."
)

AUTHOR_CONTRIBUTIONS = (
    "R.C.S. conceived the study, developed the theory, performed all analyses, generated figures, "
    "and wrote the manuscript."
)

COMPETING_INTERESTS = "The author declares no competing interests."

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
    "Valiant, L. G. A theory of the learnable. Commun. ACM 27, 1134–1142 (1984).",
]
