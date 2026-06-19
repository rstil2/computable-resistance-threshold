#!/usr/bin/env python3
"""
Fig 2 (main): expanded cross-cancer ε* vs resistance durability.

≥15 cancer types, independent L, LOO, bootstrap CI, publication figure.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from threshold import leave_one_out_correlation, load_L_table, pac_bound  # noqa: E402

NATURE_2COL = 180 / 25.4

# (label, N_e Williams, V_A Dentro, gen_err=1/TTR2 months, L_key, TTR2_source note)
CANCER_ROWS = [
    ("AML", 1200, 0.220, 0.333, "AML", "Shlush2017"),
    ("GBM", 1800, 0.195, 0.250, "GBM", "Omuro2013"),
    ("SKCM", 2750, 0.162, 0.200, "SKCM_BRAF", "Wagle2014"),
    ("HNSC", 3100, 0.155, 0.167, "HNSC", "TCGA_HNSC_median"),
    ("BRCA-TNBC", 4100, 0.141, 0.200, "BRCA_HER2", "Yates2015"),
    ("LUSC", 5100, 0.112, 0.083, "LUSC", "NSCLC_EGFR_proxy"),
    ("NSCLC-EGFR", 5050, 0.112, 0.083, "NSCLC_EGFR", "Oxnard2017"),
    ("NSCLC-ICB", 5800, 0.092, 0.100, "NSCLC_general", "Hellmann2019"),
    ("UCEC", 6200, 0.085, 0.071, "UCEC", "TCGA_UCEC"),
    ("STAD", 7000, 0.078, 0.100, "STAD", "TCGA_STAD"),
    ("CRC", 7600, 0.068, 0.125, "COADREAD_TCGA", "Osumi2021"),
    ("ESCA", 8500, 0.058, 0.143, "ESCA", "TCGA_ESCA"),
    ("LIHC", 9100, 0.052, 0.125, "LIHC", "TCGA_LIHC"),
    ("PRAD-met", 9800, 0.047, 0.083, "PRAD_ARSI", "Scher2012"),
    ("KIRC", 10400, 0.042, 0.067, "KIRC", "TCGA_KIRC"),
    ("THCA", 14200, 0.019, 0.020, "THCA", "Haugen2016"),
    ("BLCA", 5600, 0.104, 0.125, "BLCA", "TCGA_BLCA"),
]


def make_figure(df: pd.DataFrame, summary: dict, out_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(NATURE_2COL, NATURE_2COL * 1.05))

    x = df["eps_star"].values
    y = df["gen_err"].values
    colors = plt.cm.viridis(np.linspace(0.15, 0.85, len(df)))

    # Manual label offsets (points) for crowded clusters
    label_offsets = {
        "NSCLC-EGFR": (6, -10),
        "LUSC": (-4, 8),
        "BLCA": (6, 4),
        "STAD": (-8, -6),
        "CRC": (6, -4),
        "PRAD-met": (6, 2),
        "KIRC": (-10, 4),
        "THCA": (6, 2),
    }

    for i, row in df.iterrows():
        ax.scatter(row["eps_star"], row["gen_err"], s=60, color=colors[i], zorder=3, edgecolors="white", lw=0.6)
        dx, dy = label_offsets.get(row["label"], (4, 4))
        ax.annotate(
            row["label"],
            (row["eps_star"], row["gen_err"]),
            textcoords="offset points", xytext=(dx, dy),
            fontsize=7.5, va="bottom", ha="left",
            arrowprops=dict(arrowstyle="-", color="0.6", lw=0.5, shrinkA=2, shrinkB=2),
        )

    m, b, r, p, _ = stats.linregress(x, y)
    xx = np.linspace(x.min() * 0.85, x.max() * 1.08, 100)
    ax.plot(xx, m * xx + b, color="0.25", lw=1.5, ls="--")

    ax.set_xlabel(r"PAC bound $\varepsilon^*(N_e, V_A, L)$", fontsize=10)
    ax.set_ylabel(r"Resistance instability ($1/\mathrm{TTR}_2$, months$^{-1}$)", fontsize=10)
    ax.tick_params(labelsize=9)
    ax.set_title("Cross-cancer validation (independent $L$)", loc="left", fontsize=11, pad=10)

    ci = summary["bootstrap_r_ci_low"], summary["bootstrap_r_ci_high"]
    ax.text(
        0.97, 0.05,
        f"Pearson $r$ = {summary['pearson_r']:.2f}  ($p$ = {summary['pearson_p']:.2e})\n"
        f"LOO $r$ = {summary['loo_r_mean']:.2f}  (min {summary['loo_r_min']:.2f})\n"
        f"Bootstrap 95% CI: [{ci[0]:.2f}, {ci[1]:.2f}]  ($n$ = {len(df)} types)",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=8,
        bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="0.8", alpha=0.95),
    )
    fig.tight_layout(pad=1.2)
    fig.savefig(out_dir / "fig2_cross_cancer.pdf", dpi=300)
    fig.savefig(out_dir / "fig2_cross_cancer.png", dpi=300)
    plt.close()


def main() -> None:
    L_table = load_L_table()
    rows = []
    for label, Ne, VA, gen_err, L_key, _src in CANCER_ROWS:
        L = L_table.get(L_key, L_table["DEFAULT"])
        eps = pac_bound(Ne, VA, L)
        rows.append({
            "label": label, "Ne": Ne, "VA": VA, "L": L,
            "eps_star": eps, "gen_err": gen_err, "TTR2_months": 1 / gen_err,
        })

    df = pd.DataFrame(rows)
    r, p = stats.pearsonr(df["eps_star"], df["gen_err"])
    loo = leave_one_out_correlation(df["eps_star"].values, df["gen_err"].values)

    rng = np.random.default_rng(42)
    boot_rs = []
    for _ in range(10000):
        idx = rng.integers(0, len(df), len(df))
        boot_rs.append(stats.pearsonr(df["eps_star"].iloc[idx], df["gen_err"].iloc[idx]).statistic)

    out_dir = ROOT / "data" / "fig2_cross_cancer"
    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_dir / "cross_cancer_table.csv", index=False)

    summary = {
        "pearson_r": float(r), "pearson_p": float(p),
        "loo_r_mean": loo["r_mean"], "loo_r_min": loo["r_min"],
        "bootstrap_r_ci_low": float(np.percentile(boot_rs, 2.5)),
        "bootstrap_r_ci_high": float(np.percentile(boot_rs, 97.5)),
        "n_types": len(df),
    }
    pd.DataFrame([summary]).to_csv(out_dir / "summary.csv", index=False)

    sens = []
    for mult in (0.5, 1.0, 2.0):
        eps = [pac_bound(r.Ne, r.VA, max(1, int(r.L * mult))) for r in df.itertuples()]
        rr, pp = stats.pearsonr(eps, df["gen_err"])
        sens.append({"L_multiplier": mult, "pearson_r": rr, "p": pp})
    pd.DataFrame(sens).to_csv(out_dir / "L_sensitivity.csv", index=False)

    make_figure(df, summary, out_dir)
    print("Fig 2 cross-cancer:", summary)
    print(f"Wrote {out_dir}")


if __name__ == "__main__":
    main()
