#!/usr/bin/env python3
"""Power calculation for Fig 4 binary resistance outcomes."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from fig4_simulation import resistance_probability  # noqa: E402
from threshold import ne_star  # noqa: E402


def power_two_proportion(n1, n2, p1, p2, alpha=0.05):
    """Normal-approx power for two-proportion z-test."""
    p_pool = (n1 * p1 + n2 * p2) / (n1 + n2)
    se = math.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    if se == 0:
        return 0.0
    z = (abs(p1 - p2) - 0) / se
    z_alpha = 1.96
    from scipy import stats
    return float(1 - stats.norm.cdf(z_alpha - z))


def main():
    cfg = yaml.safe_load(open(ROOT / "config" / "fig4_experiment.yaml"))
    reps = cfg["replicates_per_arm"]
    fracs = cfg["arm_fractions"]

    lines = []
    for sys in cfg["systems"]:
        nstar = ne_star(VA=sys["V_A"], L=sys["L"])
        p_low = resistance_probability(nstar * fracs[0], nstar)
        p_high = resistance_probability(nstar * fracs[-1], nstar)
        pw = power_two_proportion(reps, reps, p_low, p_high)
        lines.append({
            "system": sys["id"],
            "N_e_star": round(nstar, 1),
            "p_resist_low_arm": round(p_low, 3),
            "p_resist_high_arm": round(p_high, 3),
            "replicates_per_arm": reps,
            "power_low_vs_high_arm": round(pw, 3),
        })
        print(f"{sys['id']}: N_e*={nstar:.0f}  P(resist|0.05*)={p_low:.2f}  P(resist|10*)={p_high:.2f}  power≈{pw:.2f}")

    out = ROOT / "data" / "fig4" / "power_summary.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    import pandas as pd
    pd.DataFrame(lines).to_csv(out, index=False)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
