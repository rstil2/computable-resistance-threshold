"""
Core threshold mathematics — fixed constants, independent L.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, Optional

import numpy as np

DEFAULT_EPSILON = 0.05
DEFAULT_DELTA = 0.05

_CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


def load_L_table(path: Optional[Path] = None) -> Dict[str, int]:
    """Load cancer-type → driver locus count from TSV (independent of N_e)."""
    path = path or (_CONFIG_DIR / "driver_loci_L.tsv")
    table: Dict[str, int] = {}
    with open(path) as fh:
        for line in fh:
            parts = line.strip().split("\t")
            if len(parts) < 2 or parts[0].startswith("#"):
                continue
            if parts[0] == "cancer_type":
                continue
            try:
                table[parts[0]] = int(parts[1])
            except ValueError:
                continue
    return table


def pac_bound(
    Ne: float,
    VA: float,
    L: int,
    *,
    delta: float = DEFAULT_DELTA,
) -> float:
    """
    Evolutionary PAC bound ε*(N_e, V_A, L) from Theorem 5.

    ε* = sqrt(2 V_A [L ln(e N_e / L) + ln(4/δ)] / N_e)
    """
    Ne = max(float(Ne), 1.0)
    VA = max(float(VA), 1e-9)
    L = max(int(L), 1)
    M = math.e * Ne / L
    lm = L * math.log(M) + math.log(4.0 / delta)
    return math.sqrt(2.0 * VA * lm / Ne)


def pac_failure_probability(
    Ne: float,
    VA: float,
    L: int,
    *,
    epsilon: float = DEFAULT_EPSILON,
    delta: float = DEFAULT_DELTA,
) -> float:
    """
    Approximate PAC failure probability (Theorem 5 structure).
    Used to invert for N_e*.
    """
    Ne = max(float(Ne), 1.0)
    VA = max(float(VA), 1e-9)
    L = max(int(L), 1)
    prefactor = 4.0 * (math.e * Ne / L) ** L
    exponent = -Ne * epsilon**2 / (2.0 * VA)
    return prefactor * math.exp(exponent)


def ne_star(
    VA: float,
    L: int,
    *,
    epsilon: float = DEFAULT_EPSILON,
    delta: float = DEFAULT_DELTA,
    ne_min: float = 10.0,
    ne_max: float = 1e8,
) -> float:
    """
    Minimum effective population size N_e* for reliable ε-accurate resistance evolution.

    Solve P(failure) <= δ for N_e via bisection on the monotone (decreasing) tail.
    Falls back to closed-form sample-complexity lower bound if bisection fails.
    """
    VA = max(float(VA), 1e-9)
    L = max(int(L), 1)

    def failure(Ne: float) -> float:
        return pac_failure_probability(Ne, VA, L, epsilon=epsilon, delta=delta)

    # Closed-form lower bound from Corollary 6 (starting point)
    lb = max(ne_min, 2.0 * VA / epsilon**2 * (L + math.log(4.0 / delta)))

    lo, hi = lb, ne_max
    if failure(hi) > delta:
        # Even at maximum N_e, bound not satisfied — return hi as conservative threshold
        return hi

    while failure(lo) > delta and lo > ne_min:
        lo /= 2.0
    lo = max(lo, ne_min)

    for _ in range(80):
        mid = (lo + hi) / 2.0
        if failure(mid) <= delta:
            hi = mid
        else:
            lo = mid
    return hi


def classify_patient(
    Ne: float,
    VA: float,
    L: int,
    *,
    epsilon: float = DEFAULT_EPSILON,
    delta: float = DEFAULT_DELTA,
) -> Dict[str, float | bool | str]:
    """Return N_e*, ratio, and above/below label for one patient."""
    nstar = ne_star(VA, L, epsilon=epsilon, delta=delta)
    ratio = Ne / nstar if nstar > 0 else float("inf")
    return {
        "N_e": Ne,
        "V_A": VA,
        "L": L,
        "N_e_star": nstar,
        "N_e_ratio": ratio,
        "above_threshold": Ne >= nstar,
        "epsilon_star": pac_bound(Ne, VA, L, delta=delta),
    }


def leave_one_out_correlation(
    eps_star: np.ndarray,
    outcome: np.ndarray,
) -> Dict[str, float]:
    """Leave-one-cancer-out Pearson r for Fig 3 sensitivity."""
    from scipy import stats

    n = len(eps_star)
    rs = []
    for i in range(n):
        mask = np.ones(n, dtype=bool)
        mask[i] = False
        if mask.sum() < 3:
            continue
        r, _ = stats.pearsonr(eps_star[mask], outcome[mask])
        rs.append(r)
    return {
        "r_mean": float(np.mean(rs)) if rs else float("nan"),
        "r_min": float(np.min(rs)) if rs else float("nan"),
        "r_max": float(np.max(rs)) if rs else float("nan"),
    }
