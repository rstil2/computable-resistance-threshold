#!/usr/bin/env python3
"""
Fig 3: patient-level targeted therapy (BRAF inhibitor cohorts).

Primary: Cox on log10(N_e/N_e*) with duration on therapy.
Secondary: logistic early resistance ~ log10(N_e/N_e*).
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from calibration import calibrate_ne  # noqa: E402
from cbioportal import fetch_patient_table, patient_vaf_map, parse_purity  # noqa: E402
from estimators import estimate_patient_metrics  # noqa: E402
from threshold import classify_patient, load_L_table  # noqa: E402

try:
    from lifelines import CoxPHFitter, KaplanMeierFitter
    from lifelines.statistics import logrank_test
except ImportError:
    raise SystemExit("pip install lifelines")

NATURE_2COL = 180 / 25.4

TARGETED_COHORTS = [
    {
        "study_id": "skcm_broad_brafresist_2012",
        "cancer_type": "SKCM_BRAF",
        "name": "BRAF inhibitor (Broad 2012)",
        "time_field": "DURATION_OF_THERAPY_WEEKS",
        "time_scale": 12 / 52,
        "event_from": "early_resistance",
    },
]


def parse_braf_row(row: dict, cohort: dict) -> tuple[float, bool]:
    raw = row.get(cohort["time_field"], "")
    if not raw:
        return float("nan"), False
    t = float(raw) * cohort.get("time_scale", 1.0)
    event = row.get("EARLY_RESISTANCE") == "Yes"
    if row.get("TREATMENT_BEST_RESPONSE") == "PD":
        event = True
    return t, event


def build_cohort_df(cohort: dict, L_table: dict) -> pd.DataFrame:
    sid = cohort["study_id"]
    L = L_table.get(cohort["cancer_type"], 10)
    vafs_map = patient_vaf_map(sid)

    raw_nes = []
    rows_tmp = []
    for row in fetch_patient_table(sid):
        pid = row["patientId"]
        v = vafs_map.get(pid)
        if not v:
            continue
        m = estimate_patient_metrics(v, tumor_purity=parse_purity(row))
        if math.isnan(m["N_e_sfs_raw"]):
            continue
        raw_nes.append(m["N_e_sfs_raw"])
        rows_tmp.append((row, m))

    if not raw_nes:
        return pd.DataFrame()

    med_raw = float(np.median(raw_nes))
    records = []
    for row, m in rows_tmp:
        t, event = parse_braf_row(row, cohort)
        if pd.isna(t):
            continue
        ne = calibrate_ne(m["N_e_sfs_raw"], med_raw, cohort["cancer_type"])
        cls = classify_patient(ne, m["V_A_math"], L)
        records.append({
            "study_id": sid,
            "patientId": row["patientId"],
            "time_months": t,
            "event": int(event),
            "early_resistance": row.get("EARLY_RESISTANCE") == "Yes",
            "N_e": ne,
            "N_e_star": cls["N_e_star"],
            "log10_ratio": math.log10(max(cls["N_e_ratio"], 0.01)),
            "above_threshold": cls["above_threshold"],
            "V_A": cls["V_A"],
        })
    return pd.DataFrame(records)


def cox_summary(df: pd.DataFrame) -> dict:
    cox_df = df[["time_months", "event", "log10_ratio"]].copy()
    cph = CoxPHFitter()
    cph.fit(cox_df, duration_col="time_months", event_col="event")
    s = cph.summary.loc["log10_ratio"]
    from scipy import stats
    rho, rho_p = stats.spearmanr(df["log10_ratio"], df["time_months"])
    return {
        "HR": float(s["exp(coef)"]),
        "HR_low": float(s["exp(coef) lower 95%"]),
        "HR_high": float(s["exp(coef) upper 95%"]),
        "p": float(s["p"]),
        "spearman_rho": float(rho),
        "spearman_p": float(rho_p),
        "n": len(df),
        "events": int(df["event"].sum()),
    }


def logistic_early_resist(df: pd.DataFrame) -> dict:
    from scipy.special import expit
    from scipy.optimize import minimize

    y = df["early_resistance"].astype(float).values
    x = df["log10_ratio"].values
    X = np.column_stack([np.ones(len(x)), x])

    def nll(b):
        p = expit(X @ b)
        return -np.sum(y * np.log(p + 1e-9) + (1 - y) * np.log(1 - p + 1e-9))

    res = minimize(nll, [0, 0.5], method="L-BFGS-B")
    b0, b1 = res.x
    from scipy import stats
    # Wald SE rough
    p_hat = expit(X @ res.x)
    w = p_hat * (1 - p_hat)
    cov = np.linalg.inv(X.T * w @ X)
    se = np.sqrt(cov[1, 1])
    z = b1 / se
    pval = 2 * (1 - stats.norm.cdf(abs(z)))
    return {"OR_per_log10": float(np.exp(b1)), "p": float(pval), "n": len(y)}


def make_figure(df: pd.DataFrame, cox: dict, logistic: dict, out_dir: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(NATURE_2COL, NATURE_2COL * 0.52))

    # Panel A: scatter duration vs log ratio
    ax = axes[0]
    colors = ["#D6604D" if e else "#2166AC" for e in df["early_resistance"]]
    ax.scatter(df["log10_ratio"], df["time_months"], c=colors, s=45, alpha=0.85, edgecolors="white", linewidths=0.4)
    ax.set_xlabel(r"$\log_{10}(N_e / N_e^*)$", fontsize=10)
    ax.set_ylabel("Duration on BRAF inhibitor (months)", fontsize=10)
    ax.tick_params(labelsize=9)
    ax.text(0.0, 1.06, "A", transform=ax.transAxes, fontsize=13, fontweight="bold", va="bottom")
    ax.text(0.045, 1.06, "Vemurafenib cohort (n = 45)", transform=ax.transAxes, fontsize=10, fontweight="bold", va="bottom")

    # Legend for point colours
    from matplotlib.lines import Line2D
    ax.legend(
        handles=[
            Line2D([0], [0], marker="o", color="w", markerfacecolor="#2166AC", markersize=8, label="No early resistance"),
            Line2D([0], [0], marker="o", color="w", markerfacecolor="#D6604D", markersize=8, label="Early resistance"),
        ],
        loc="upper right", fontsize=8, framealpha=0.9,
    )

    # Panel B: boxplot by early resistance (avoid pandas auto-suptitle)
    ax2 = axes[1]
    no_er = df.loc[~df["early_resistance"], "time_months"]
    er = df.loc[df["early_resistance"], "time_months"]
    bp = ax2.boxplot(
        [no_er, er],
        tick_labels=["No early\nresistance", "Early\nresistance"],
        patch_artist=True,
        widths=0.55,
    )
    for patch, c in zip(bp["boxes"], ["#2166AC", "#D6604D"]):
        patch.set_facecolor(c)
        patch.set_alpha(0.55)
    ax2.set_ylabel("Months on therapy", fontsize=10)
    ax2.tick_params(labelsize=9)
    ax2.text(0.0, 1.06, "B", transform=ax2.transAxes, fontsize=13, fontweight="bold", va="bottom")
    ax2.text(0.045, 1.06, "Duration by resistance phenotype", transform=ax2.transAxes, fontsize=10, fontweight="bold", va="bottom")

    stats_txt = (
        f"Cox HR = {cox['HR']:.2f} ({cox['HR_low']:.2f}–{cox['HR_high']:.2f}), P = {cox['p']:.3g}   "
        f"Spearman ρ = {cox['spearman_rho']:.2f}, P = {cox['spearman_p']:.3g}   "
        f"Early-resist OR = {logistic['OR_per_log10']:.2f}, P = {logistic['p']:.3g}"
    )
    fig.text(0.5, 0.01, stats_txt, ha="center", fontsize=8, color="0.35")

    fig.subplots_adjust(left=0.09, right=0.98, top=0.78, bottom=0.16, wspace=0.28)
    fig.savefig(out_dir / "fig3_targeted_therapy.pdf", dpi=300)
    fig.savefig(out_dir / "fig3_targeted_therapy.png", dpi=300)
    plt.close()


def main() -> None:
    L_table = load_L_table()
    out_dir = ROOT / "data" / "fig3_targeted"
    out_dir.mkdir(parents=True, exist_ok=True)

    frames = [build_cohort_df(c, L_table) for c in TARGETED_COHORTS]
    df = pd.concat(frames, ignore_index=True)
    df.to_csv(out_dir / "braf_patients.csv", index=False)

    if len(df) < 10:
        print("Too few patients:", len(df))
        return

    cox = cox_summary(df)
    logistic = logistic_early_resist(df)
    pd.DataFrame([{**cox, **{f"logistic_{k}": v for k, v in logistic.items()}}]).to_csv(
        out_dir / "analysis_summary.csv", index=False
    )

    make_figure(df, cox, logistic, out_dir)
    print("Fig 3 targeted therapy:")
    print("  Cox:", cox)
    print("  Logistic early resistance:", logistic)
    print(f"  Below N_e*: {(~df.above_threshold).sum()} / {len(df)}")
    print(f"Wrote {out_dir}")


if __name__ == "__main__":
    main()
