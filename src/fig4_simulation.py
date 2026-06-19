"""
Wright-Fisher style simulation for Fig 4 predicted outcomes.

Generates resistance emergence probability as a function of bottleneck N_e / N_e*,
with a sharp transition at ratio = 1 (evolutionary sample complexity threshold).
"""

from __future__ import annotations

from typing import Dict, List

import numpy as np
import pandas as pd
import yaml
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from threshold import ne_star  # noqa: E402


def resistance_probability(ne: float, ne_star_val: float, *, steepness: float = 4.5) -> float:
    """
    P(resistance emerges by end of experiment).

    Logistic step in log10(N_e / N_e*): below 1, learning unreliable → low P;
    above 1, resistance discoverable → high P.
    """
    ratio = max(ne / ne_star_val, 1e-3)
    log10_r = np.log10(ratio)
    # Center transition at log10(r)=0 (i.e. N_e = N_e*)
    return float(1.0 / (1.0 + np.exp(-steepness * log10_r)))


def simulate_experiment(
    *,
    arm_fractions: List[float],
    replicates: int,
    ne_star_val: float,
    system_id: str,
    seed: int = 42,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for frac in arm_fractions:
        ne = max(ne_star_val * frac, 10.0)
        p = resistance_probability(ne, ne_star_val)
        for rep in range(replicates):
            resistant = int(rng.random() < p)
            rows.append({
                "system_id": system_id,
                "arm_fraction": frac,
                "replicate": rep + 1,
                "N_e": ne,
                "N_e_star": ne_star_val,
                "N_e_ratio": ne / ne_star_val,
                "resistance": resistant,
                "simulated": True,
            })
    return pd.DataFrame(rows)


def simulate_all_systems(config_path: Path) -> pd.DataFrame:
    cfg = yaml.safe_load(open(config_path))
    arm_fractions = cfg["arm_fractions"]
    replicates = cfg["replicates_per_arm"]
    frames = []
    for i, sys in enumerate(cfg["systems"]):
        nstar = ne_star(L=sys["L"], VA=sys["V_A"])
        df = simulate_experiment(
            arm_fractions=arm_fractions,
            replicates=replicates,
            ne_star_val=nstar,
            system_id=sys["id"],
            seed=42 + i,
        )
        df["cell_line"] = sys["cell_line"]
        df["drug"] = sys["drug"]
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


if __name__ == "__main__":
    cfg_path = ROOT / "config" / "fig4_experiment.yaml"
    out = ROOT / "data" / "fig4" / "simulated_results.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df = simulate_all_systems(cfg_path)
    df.to_csv(out, index=False)
    print(f"Wrote {out} ({len(df)} rows)")
