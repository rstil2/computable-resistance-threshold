#!/usr/bin/env python3
"""
Fig 4: clinical utility — distribution of N_e/N_e* at sequencing across cohorts.

Shows what fraction of patients exceed the resistance-learnability threshold.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from calibration import calibrate_ne  # noqa: E402
from cbioportal import fetch_patient_table, patient_vaf_map, parse_purity  # noqa: E402
from estimators import estimate_patient_metrics  # noqa: E402
from threshold import classify_patient, load_L_table  # noqa: E402

NATURE_2COL = 180 / 25.4

COHORTS = [
    ("luad_tcga_pan_can_atlas_2018", "LUAD_TCGA", "NSCLC"),
    ("skcm_tcga_pan_can_atlas_2018", "SKCM_TCGA", "Melanoma"),
    ("coadread_tcga_pan_can_atlas_2018", "COADREAD_TCGA", "Colorectal"),
    ("skcm_broad_brafresist_2012", "SKCM_BRAF", "Melanoma (BRAF)"),
]


def cohort_ratios(study_id: str, cancer_type: str, label: str, L_table: dict) -> pd.DataFrame:
    L = L_table.get(cancer_type, L_table["DEFAULT"])
    vafs_map = patient_vaf_map(study_id)
    raw_list = []
    tmp = []
    for row in fetch_patient_table(study_id):
        v = vafs_map.get(row["patientId"])
        if not v:
            continue
        m = estimate_patient_metrics(v, tumor_purity=parse_purity(row))
        if math.isnan(m.get("N_e_sfs_raw", float("nan"))):
            continue
        raw_list.append(m["N_e_sfs_raw"])
        tmp.append((row, m))

    if not raw_list:
        return pd.DataFrame()

    med = float(np.median(raw_list))
    rows = []
    for row, m in tmp:
        ne = calibrate_ne(m["N_e_sfs_raw"], med, cancer_type)
        cls = classify_patient(ne, m["V_A_math"], L)
        rows.append({
            "study_id": study_id,
            "label": label,
            "N_e_ratio": cls["N_e_ratio"],
            "log10_ratio": math.log10(max(cls["N_e_ratio"], 0.01)),
            "above_threshold": cls["above_threshold"],
        })
    return pd.DataFrame(rows)


def main() -> None:
    L_table = load_L_table()
    out_dir = ROOT / "data" / "fig4_utility"
    out_dir.mkdir(parents=True, exist_ok=True)

    frames = [cohort_ratios(s, ct, lb, L_table) for s, ct, lb in COHORTS]
    df = pd.concat(frames, ignore_index=True)
    df.to_csv(out_dir / "patient_ratios.csv", index=False)

    # Summary table
    summary = df.groupby("label").agg(
        n=("above_threshold", "size"),
        pct_above=("above_threshold", "mean"),
        median_ratio=("N_e_ratio", "median"),
    ).reset_index()
    summary["pct_above"] *= 100
    summary.to_csv(out_dir / "summary_by_cohort.csv", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(NATURE_2COL, NATURE_2COL * 0.52))

    ax = axes[0]
    ax.hist(df["log10_ratio"], bins=30, color="#2166AC", alpha=0.75, edgecolor="white")
    ax.axvline(0, color="#D6604D", ls="--", lw=1.5, label=r"$N_e = N_e^*$")
    ax.set_xlabel(r"$\log_{10}(N_e / N_e^*)$", fontsize=10)
    ax.set_ylabel("Patients", fontsize=10)
    ax.tick_params(labelsize=9)
    ax.text(0.0, 1.04, "A", transform=ax.transAxes, fontsize=13, fontweight="bold", va="bottom")
    ax.text(0.05, 1.04, f"Threshold ratio at sequencing (n = {len(df)})", transform=ax.transAxes, fontsize=10, fontweight="bold", va="bottom")
    ax.legend(fontsize=8, loc="upper right")

    ax2 = axes[1]
    labels = summary["label"].tolist()
    pcts = summary["pct_above"].tolist()
    colors = ["#D6604D" if p > 50 else "#2166AC" for p in pcts]
    ax2.barh(range(len(labels)), pcts, color=colors, height=0.55)
    ax2.set_yticks(range(len(labels)))
    ax2.set_yticklabels(labels, fontsize=9)
    ax2.set_xlabel(r"% patients with $N_e \geq N_e^*$", fontsize=10)
    ax2.set_xlim(0, 100)
    ax2.tick_params(labelsize=9)
    ax2.text(0.0, 1.04, "B", transform=ax2.transAxes, fontsize=13, fontweight="bold", va="bottom")
    ax2.text(0.05, 1.04, "Above threshold by cohort", transform=ax2.transAxes, fontsize=10, fontweight="bold", va="bottom")
    for i, p in enumerate(pcts):
        ax2.text(min(p + 2, 92), i, f"{p:.0f}%", va="center", fontsize=8)

    fig.subplots_adjust(left=0.12, right=0.98, top=0.82, bottom=0.14, wspace=0.35)
    fig.savefig(out_dir / "fig4_clinical_utility.pdf", dpi=300)
    fig.savefig(out_dir / "fig4_clinical_utility.png", dpi=300)
    plt.close()

    print("Clinical utility summary:")
    print(summary.to_string(index=False))
    print(f"Wrote {out_dir}")


if __name__ == "__main__":
    main()
