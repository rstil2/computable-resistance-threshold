# Abstract (draft, ~175 words)

Drug resistance remains the dominant cause of cancer treatment failure, yet clinicians rarely receive a quantitative forecast of resistance risk before starting therapy. Here we define **N_e\***, a resistance-learnability threshold computable from standard tumour sequencing—subclonal diversity (V_A), effective population size (N_e), and an independently specified count of resistance-relevant driver loci (L). N_e\* marks the minimum population size at which evolution can reliably produce fit resistant clones under a fixed tolerance (ε = 0.05).

Across **seventeen cancer types**, the theoretical PAC bound ε\* correlates with published resistance durability (Pearson **r = 0.88**, leave-one-out minimum **r = 0.77**), supporting a pan-cancer resistance ecology independent of patient-level fitting. In the largest public vemurafenib cohort with resistance-specific annotations (**n = 45**), pre-registered continuous association of log(N_e/N_e\*) with time on therapy was **null** (Cox **P = 0.97**), consistent with limited events and stratum imbalance. Distribution analyses show N_e\* can be computed from fields already on most sequencing reports, with **2–28%** of patients exceeding the threshold depending on indication.

Our findings offer a computable pre-treatment stratifier anchored in evolutionary sample complexity—not a treatment algorithm and not a causal proof. Pre-registered generic progression-free survival analyses were null, underscoring the need for resistance-specific endpoints in future validation.

---

**Keywords:** drug resistance, effective population size, tumour heterogeneity, evolutionary oncology, precision medicine

**Data availability:** cBioPortal public cohorts; analysis code and locked configuration at [GitHub/Zenodo URL TBD], OSF https://osf.io/kp5jf
