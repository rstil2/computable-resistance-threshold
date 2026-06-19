# Reframed paper plan — Nature Cancer / Nature Communications

**No wet lab (no Fig 4/5).**  
**Honest claim:** A resistance-learnability threshold N_e* is **computable from standard sequencing** and **predicts resistance ecology** at the cancer-type and (where endpoints permit) patient level — not that we causally manipulated N_e in vitro.

**OSF locked:** https://osf.io/kp5jf

---

## One-sentence thesis (revised)

> Resistance evolution has a sample-complexity threshold N_e* that can be computed at diagnosis from sequencing; tumours above N_e* show faster resistance emergence where the clinical endpoint actually measures resistance on targeted therapy.

---

## Figure spine (4 main figures + ED)

| Fig | Role | Content |
|-----|------|---------|
| **1** | Clinical hook | N_e* formula + **mock sequencing report** (V_A, h², N_e, N_e* annotated) |
| **2** | **Primary empirical spine** | Hardened **cross-cancer** ε* vs resistance durability (independent L, LOO, bootstrap, ≥12 types if data allow) |
| **3** | **Patient-level validation** | **Targeted-therapy cohorts only** (BRAF resist + MSK BRAF); duration-to-resistance / early resistance; continuous log(N_e/N_e*) Cox |
| **4** | **Clinical utility** | Distribution of N_e* at “diagnosis” across TCGA/MSK; % patients above threshold by cancer type; which reports already contain inputs |

**Extended Data (not headline):**
- TCGA PFS null (pre-registered attempt + why it failed: wrong endpoint, imbalance)
- Estimator sensitivity (N_e methods, L multipliers)
- Immune / PD-1 panel (r≈0.15 — demoted)
- Theory → Supplementary Note 1 only

**Drop from main text:** Fig 4 barcoded experiment, Fig 5 organoids, causal language.

---

## What already works (keep)

- **Cross-cancer Fig 3:** r ≈ 0.94, independent L, LOO robust → **promote to Fig 2**
- **OSF pre-registration:** credibility; report TCGA as pre-specified null, not hidden
- **Computability:** V_A + L + N_e from standard outputs
- **Theory:** one paragraph + supplement (readers can ignore ML)

---

## What hurt us (fix or demote)

| Problem | Fix |
|---------|-----|
| TCGA PFS ≠ resistance | Move to ED; don’t lead patient claims with it |
| Binary split at N_e* imbalanced (~94% above) | **Primary patient analysis: continuous log(N_e/N_e*)** (pre-reg H2); binary KM as secondary |
| N_e estimator rough | Calibrate to Williams medians; report two estimators |
| Small BRAF n | Pool MSK BRAF 2024 + Broad 2012 for Fig 3 patient panel |
| n=9 cancer types | Expand to PCAWG + published TTR₂ table (target 12–15) |

---

## Strengthening work (priority order)

### Tier A — Do now (computational, no new data access)

1. **Promote & expand cross-cancer analysis** (`scripts/04_fig3_cross_cancer.py`)
   - Add cancer types from PCAWG Extended Data / Williams Table S1
   - Fig: ε* vs 1/TTR₂ with LOO shading, bootstrap CI band
   - Table: all parameters + sources

2. **Targeted-therapy patient panel** (new `scripts/07_fig3_patient_targeted.py`)
   - Cohorts: `skcm_broad_brafresist_2012`, `braf_msk_impact_2024`, `braf_msk_archer_2024`
   - Endpoint: duration on drug / early resistance (not generic PFS)
   - Primary: Cox HR for log(N_e/N_e*)
   - Secondary: KM if ≥5 per arm below N_e*

3. **N_e calibration pass** (`src/estimators.py`)
   - Anchor median N_e to Williams per cancer type in validation set
   - Report primary + cellularity secondary in all patient plots

4. **Fig 1 clinical mock-up** (`scripts/02_fig1_clinical.py`)
   - Realistic NGS report with N_e* callout box

5. **Fig 4 → clinical utility panel** (`scripts/08_fig4_clinical_utility.py`)
   - Histogram of N_e/N_e* across MSK-IMPACT metastatic samples
   - “Actionable at diagnosis” fraction by cancer type

### Tier B — If access allows (still no wet lab)

6. **TRACERx EGA** (bonus, not required) — per-patient ctDNA adaptation vs N_e*
7. **Hartwig / GENIE** metastatic — resistance dated cohorts if DAC obtainable
8. **Prospective registry** — name in Discussion only; register N_e* calculator as web tool (GitHub Pages)

### Tier C — Writing (parallel)

9. **Abstract rewrite** — remove Fig 4/5 promises
10. **Discussion** — “causal test is future work”; “clinical utility is risk stratification, not treatment algorithm yet”
11. **Limitations paragraph** — PFS null, retrospective, estimator dependence (pre-empt reviewers)

---

## Venue fit

| Venue | Fit | Why |
|-------|-----|-----|
| **Nature Cancer** | Strong | Clinical framing, computable biomarker, cross-cancer + targeted subset |
| **Nature Communications** | Strong | Method + pan-cancer validation; patient n smaller OK |
| Nature / Science | Drop | Needed causal Fig 4 |
| Cell Reports Medicine | Backup | Same package, faster |

---

## Reviewer attacks → preempt

| Attack | Response |
|--------|----------|
| “Just an analogy” | Theory in supplement; empirics stand alone |
| “L circularity” | Independent L table (done) |
| “n=9 types” | Expand types; LOO |
| “Patient validation weak” | Honest TCGA null in ED; targeted cohort for Fig 3 |
| “Not actionable” | Fig 4 utility: inputs already in reports |
| “No causal proof” | Explicit limitation; cross-cancer + targeted association |

---

## 8-week execution calendar

| Week | Deliverable |
|------|-------------|
| 1 | Expand cross-cancer; recalibrate N_e; new figure numbering |
| 2 | MSK+BRAF patient Cox panel; update OSF deviation note (estimator calibration) |
| 3 | Fig 1 mock report + clinical utility Fig 4 |
| 4 | Extended Data figures + source tables |
| 5–6 | Manuscript draft (Intro, Results, Methods) |
| 7 | Internal read / biostat check on Cox models |
| 8 | Submit Nature Cancer (or Nat Commun if advised) |

---

## Success criteria (submission-ready)

- [x] Cross-cancer r > 0.85 with LOO min r > 0.75, ≥12 types (r=0.88, LOO min=0.77, n=17)
- [x] Targeted-therapy Cox: HR > 1 for log(N_e/N_e*), p < 0.05 **or** honest null with n documented (null: HR=0.97, p=0.97, n=45)
- [x] Fig 1 legible to an oncologist in 30 seconds
- [x] TCGA PFS null in ED with pre-reg citation (log-rank p=0.55 pooled; binary null)
- [ ] No causal claims in abstract (draft pending)
- [ ] Code + config on GitHub/Zenodo linked from OSF
