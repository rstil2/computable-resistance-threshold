#!/usr/bin/env python3
"""Fig 3 cross-cancer validation with independent L and LOO/bootstrap."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from threshold import leave_one_out_correlation, load_L_table, pac_bound  # noqa: E402

# Published per-cancer parameters (N_e, V_A from Williams 2016 / Dentro 2021)
# gen_err = 1 / TTR2_months — outcome independent of L
CANCER_ROWS = [
    ("AML", 1200, 0.220, 0.333, "AML"),
    ("GBM", 1800, 0.195, 0.250, "GBM"),
    ("SKCM", 2750, 0.162, 0.200, "SKCM_BRAF"),
    ("BRCA-TNBC", 4100, 0.141, 0.200, "BRCA_HER2"),
    ("NSCLC-EGFR", 5050, 0.112, 0.083, "NSCLC_EGFR"),
    ("NSCLC-ICB", 5800, 0.092, 0.100, "NSCLC_general"),
    ("CRC", 7600, 0.068, 0.125, "COADREAD_TCGA"),
    ("PRAD-met", 9800, 0.047, 0.083, "PRAD_ARSI"),
    ("THCA", 14200, 0.019, 0.020, "THCA"),
]


def main() -> None:
    L_table = load_L_table()
    rows = []
    for label, Ne, VA, gen_err, L_key in CANCER_ROWS:
        L = L_table[L_key]
        eps = pac_bound(Ne, VA, L)
        rows.append({"label": label, "Ne": Ne, "VA": VA, "L": L, "eps_star": eps, "gen_err": gen_err})

    df = pd.DataFrame(rows)
    r, p = stats.pearsonr(df["eps_star"], df["gen_err"])
    loo = leave_one_out_correlation(df["eps_star"].values, df["gen_err"].values)

    rng = np.random.default_rng(42)
    boot_rs = []
    for _ in range(10000):
        idx = rng.integers(0, len(df), len(df))
        boot_rs.append(stats.pearsonr(df["eps_star"].iloc[idx], df["gen_err"].iloc[idx]).statistic)

    out_dir = ROOT / "data" / "fig3"
    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_dir / "cross_cancer_eps_star.csv", index=False)

    summary = {
        "pearson_r": float(r),
        "pearson_p": float(p),
        "loo_r_mean": loo["r_mean"],
        "loo_r_min": loo["r_min"],
        "bootstrap_r_ci_low": float(np.percentile(boot_rs, 2.5)),
        "bootstrap_r_ci_high": float(np.percentile(boot_rs, 97.5)),
    }
    pd.DataFrame([summary]).to_csv(out_dir / "fig3_summary.csv", index=False)

    # L sensitivity
    sens = []
    for mult in (0.5, 1.0, 2.0):
        eps = [pac_bound(r.Ne, r.VA, max(1, int(r.L * mult))) for r in df.itertuples()]
        rr, _ = stats.pearsonr(eps, df["gen_err"])
        sens.append({"L_multiplier": mult, "pearson_r": rr})
    pd.DataFrame(sens).to_csv(out_dir / "L_sensitivity.csv", index=False)

    print("Fig 3 summary:", summary)
    print(f"Wrote {out_dir}")


if __name__ == "__main__":
    main()
