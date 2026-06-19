#!/usr/bin/env python3
"""
Generate Fig 4: causal bottleneck experiment.

Uses simulated data until lab CSV is provided at data/fig4/lab_results.csv.
Replace simulated_results.csv with real data — same schema, same script.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fig4_analysis import fit_changepoint_logistic, fit_primary_logistic, summarize_by_arm  # noqa: E402
from fig4_simulation import simulate_all_systems  # noqa: E402

NATURE_2COL = 180 / 25.4
C = {"blue": "#2166AC", "red": "#D6604D", "grey": "#878787", "orange": "#F4A442"}


def panel_schematic(ax):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title("A  Experimental design", loc="left", fontsize=10, fontweight="bold")

    boxes = [
        (0.5, 6.5, "Barcode\nlibrary"),
        (3.0, 6.5, "Bottleneck\npassage\n(set N_e)"),
        (5.5, 6.5, "Drug selection\n(fixed IC80)"),
        (8.0, 6.5, "Resistance\nreadout"),
    ]
    for i, (x, y, txt) in enumerate(boxes):
        ax.add_patch(mpatches.FancyBboxPatch((x, y), 1.8, 2.0, boxstyle="round,pad=0.05",
                     fc=C["blue"] if i == 1 else "0.92", ec="0.4", lw=1))
        ax.text(x + 0.9, y + 1.0, txt, ha="center", va="center", fontsize=7)
        if i < len(boxes) - 1:
            ax.annotate("", xy=(x + 2.0, y + 1.0), xytext=(x + 1.85, y + 1.0),
                        arrowprops=dict(arrowstyle="-|>", lw=1.2, color="0.3"))

    ax.text(5, 4.8, r"Arms: $N_e \in \{0.05, 0.2, 0.5, 1, 2, 10\} \times N_e^*$",
            ha="center", fontsize=8)
    ax.text(5, 3.8, "N_e* from parental WES (V_A, L) — fixed before experiment",
            ha="center", fontsize=7, color="0.45", style="italic")
    ax.text(5, 1.2, "Prediction: P(resistance) collapses below $N_e = N_e^*$, not smooth gradient",
            ha="center", fontsize=8, color=C["red"])


def panel_results(ax, df: pd.DataFrame, system_id: str, panel_label: str, title: str):
    sub = df[df.system_id == system_id].copy()
    arm = summarize_by_arm(sub)
    x = np.log10(arm["ratio_mean"])

    ax.errorbar(
        x, arm["p_resistance"], yerr=[arm["p_resistance"] - arm["ci_low"], arm["ci_high"] - arm["p_resistance"]],
        fmt="o", color=C["blue"], ecolor="0.35", capsize=3, ms=6, lw=1, label="Observed ± 95% CI",
    )

    # Jitter replicates
    jitter = np.random.default_rng(0).normal(0, 0.04, len(sub))
    ax.scatter(
        np.log10(sub["N_e_ratio"]) + jitter,
        sub["resistance"] + jitter * 0.02,
        s=12, alpha=0.35, color=C["grey"], lw=0, zorder=1,
    )

    # Primary logistic on replicate-level data
    fit = fit_primary_logistic(sub)
    xx = np.linspace(x.min() - 0.3, x.max() + 0.3, 100)
    eta = fit["intercept"] + fit["coef_log10_ratio"] * xx
    yy = 1 / (1 + np.exp(-eta))
    ax.plot(xx, yy, color=C["red"], lw=1.5, label="Logistic fit")

    ax.axvline(0, color=C["orange"], ls="--", lw=1.2, label=r"$N_e = N_e^*$")

    cp = fit_changepoint_logistic(sub, cp_log10=0.0)
    ax.text(
        0.02, 0.98,
        f"Primary logistic: OR/log10={fit['odds_ratio_per_log10']:.2f}, p={fit['p_log10_ratio']:.3g}\n"
        f"Changepoint AIC Δ={cp.aic_single - cp.aic_piecewise:.1f}, Chow p={cp.p_chow:.3g}",
        transform=ax.transAxes, va="top", fontsize=6.5,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="0.8", alpha=0.9),
    )

    ax.set_xlabel(r"$\log_{10}(N_e / N_e^*)$")
    ax.set_ylabel("P(resistance emergence)")
    ax.set_ylim(-0.05, 1.05)
    ax.set_title(f"{panel_label}  {title}", loc="left", fontsize=10, fontweight="bold")
    ax.legend(fontsize=6, loc="lower right")


def main():
    cfg_path = ROOT / "config" / "fig4_experiment.yaml"
    cfg = yaml.safe_load(open(cfg_path))
    out_dir = ROOT / "data" / "fig4"
    out_dir.mkdir(parents=True, exist_ok=True)

    lab_path = out_dir / "lab_results.csv"
    sim_path = out_dir / "simulated_results.csv"

    if lab_path.exists():
        df = pd.read_csv(lab_path)
        data_label = "Experimental data"
        print("Using lab_results.csv")
    else:
        df = simulate_all_systems(cfg_path)
        df.to_csv(sim_path, index=False)
        data_label = "Simulated (pre-registered design — replace with lab data)"
        print(f"Using simulation → {sim_path}")

    systems = cfg["systems"]
    fig, axes = plt.subplots(1, 3, figsize=(NATURE_2COL, NATURE_2COL * 0.38))
    panel_schematic(axes[0])
    for ax, sys, lbl in zip(axes[1:], systems, ["B", "C"]):
        panel_results(
            ax, df, sys["id"], lbl,
            f"{sys['cell_line']} + {sys['drug']}",
        )

    fig.suptitle(
        f"Fig 4 — Causal threshold ({data_label})",
        fontsize=9, y=1.02, color="0.35" if "Simulated" in data_label else "0.1",
    )
    fig.tight_layout()
    pdf = out_dir / "fig4_causal_threshold.pdf"
    png = out_dir / "fig4_causal_threshold.png"
    fig.savefig(pdf, dpi=300, bbox_inches="tight")
    fig.savefig(png, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved {pdf}")

    # Analysis summary
    rows = []
    for sys in systems:
        sub = df[df.system_id == sys["id"]]
        fit = fit_primary_logistic(sub)
        cp = fit_changepoint_logistic(sub)
        rows.append({"system_id": sys["id"], **fit, "chow_p": cp.p_chow})
    pd.DataFrame(rows).to_csv(out_dir / "analysis_summary.csv", index=False)


if __name__ == "__main__":
    main()
