"""Supplementary Note 1 — PAC formalism summary (proofs in theory preprint)."""

from content import AUTHORS, THEORY_PREPRINT_DOI  # noqa: F401

TITLE = "Supplementary Note 1"
SUBTITLE = "PAC formalism for resistance learnability"

EMPIRICAL_PAPER = (
    "N_e*: a computable population-size threshold for resistance learnability "
    "from standard tumour sequencing"
)

INTRO = [
    (
        "This note summarizes the learning-theoretic objects behind N_e* for reviewers of the "
        "empirical validation paper. Full theorem statements and proofs are not reproduced here; "
        "they appear in the companion theory preprint:"
    ),
    (
        "Stillwell, R. C. Natural selection is empirical risk minimisation. Preprint at "
        f"Research Square (2026). {THEORY_PREPRINT_DOI}"
    ),
    (
        "That preprint establishes the unified empirical-risk-minimization structure linking "
        "Fisher's theorem, the Price equation, and PAC sample-complexity bounds. The empirical "
        "paper tests predictions derived from that framework without duplicating its proofs."
    ),
]

SECTIONS = [
    (
        "Instance space and hypothesis class",
        [
            (
                "Instance space X: bulk-sequencing summaries of resistance-relevant genotype "
                "structure at baseline—allele frequencies at L independently curated driver loci, "
                "together with subclonal dispersion V_A across the genome."
            ),
            (
                "Hypothesis class H: resistance phenotypes realizable by selection on a tumour "
                "effective population of size N_e with subclonal variance V_A. Each h in H "
                "specifies a distribution over resistant clone frequencies achievable within one "
                "evolutionary episode before sensitive cells are depleted."
            ),
            (
                "Target concept h*: an ε-optimal resistant phenotype—fitness within ε of the best "
                "resistance genotype discoverable at the L loci under the current therapy."
            ),
        ],
    ),
    (
        "Loss and failure event",
        [
            "Loss (per evolutionary episode):",
            "    ℓ(h) = max(0, f(h*) − f(h)),",
            (
                "where f(·) is resistance fitness under drug pressure, normalized so f(h*) = 1."
            ),
            (
                "Failure event (PAC sense): ℓ(h) > ε after search over N_e inherited units—i.e. "
                "evolution does not reach an ε-optimal resistant state with the required reliability."
            ),
            (
                "This is a continuous, Fisher-information learning problem on allele-frequency "
                "space, not binary classification. VC dimension of threshold functions on R^d is "
                "therefore not the operative capacity measure."
            ),
        ],
    ),
    (
        "Role of N_e",
        [
            (
                "N_e enters as effective sample size: the number of independently segregating "
                "units that contribute to sampling resistance alleles before selection exhausts "
                "sensitive clones. The bound is"
            ),
            "    ε*(N_e, V_A, L) = sqrt(2 V_A [L ln(e N_e / L) + ln(4/δ)] / N_e),",
            (
                "where the tail P(failure) ≤ δ follows a large-deviation (Chernoff–Hoeffding type) "
                "inequality on occupancy of resistance alleles across L loci, with V_A scaling "
                "subclonal noise. N_e is sample complexity in this stochastic search sense, "
                "analogous to m in PAC sample-size bounds but not to labeled-example count in "
                "Valiant's discrete hypothesis classes. See Stillwell (2026 preprint) for "
                "derivation under the infinitesimal model."
            ),
        ],
    ),
    (
        "Threshold N_e*",
        [
            (
                "N_e* is the smallest N_e such that P(failure) ≤ δ at tolerance ε, obtained by "
                "monotone bisection on the PAC tail (implementation: threshold.ne_star in the "
                "analysis repository)."
            ),
        ],
    ),
    (
        "Relation to empirical analyses",
        [
            (
                "Cross-cancer ecology (Fig. 2 of the empirical paper): tests whether "
                "ε*(N_e, V_A, L) covaries with published resistance kinetics when L is fixed "
                "independently. This does not require PAC identifiability to hold pointwise for "
                "every tumour."
            ),
            (
                "Patient analyses: test whether log10(N_e/N_e*) stratifies time-to-resistance "
                "when inputs are estimated from single samples."
            ),
        ],
    ),
]
