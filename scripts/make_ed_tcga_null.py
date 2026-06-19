#!/usr/bin/env python3
"""
Extended Data: pre-registered TCGA PFS analysis (calibrated N_e).

Binary KM + continuous Cox on log10(N_e/N_e*). Documents honest null on generic PFS.
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

TCGA_COHORTS = [
    {"study_id": "luad_tcga_pan_can_atlas_2018", "cancer_type": "LUAD_TCGA", "label": "LUAD"},
    {"study_id": "skcm_tcga_pan_can_atlas_2018", "cancer_type": "SKCM_TCGA", "label": "SKCM"},
    {"study_id": "coadread_tcga_pan_can_atlas_2018", "cancer_type": "COADREAD_TCGA", "label": "COADREAD"},
]


def parse_pfs(row: dict, cohort: dict) -> tuple[float, bool]:
    raw = row.get(cohort["endpoint_field"], "")
    if not raw:
        return float("nan"), False
    t = float(raw)
    status = row.get(cohort.get("endpoint_status", "PFS_STATUS"), "")
    event = "Progressed" in status or status.startswith("1:")
    return t, event


def build_cohort(cohort: dict, L_table: dict) -> pd.DataFrame:
    sid = cohort["study_id"]
    ct = cohort["cancer_type"]
    L = L_table.get(ct, L_table["DEFAULT"])
    cohort_cfg = {
        "endpoint_field": "PFS_MONTHS",
        "endpoint_status": "PFS_STATUS",
    }
    vafs_map = patient_vaf_map(sid)

    raw_nes = []
    tmp = []
    for row in fetch_patient_table(sid):
        v = vafs_map.get(row["patientId"])
        if not v:
            continue
        m = estimate_patient_metrics(v, tumor_purity=parse_purity(row))
        if math.isnan(m.get("N_e_sfs_raw", float("nan"))):
            continue
        raw_nes.append(m["N_e_sfs_raw"])
        tmp.append((row, m))

    if not raw_nes:
        return pd.DataFrame()

    med = float(np.median(raw_nes))
    records = []
    for row, m in tmp:
        t, event = parse_pfs(row, cohort_cfg)
        if pd.isna(t):
            continue
        ne = calibrate_ne(m["N_e_sfs_raw"], med, ct)
        cls = classify_patient(ne, m["V_A_math"], L)
        records.append({
            "study_id": sid,
            "label": cohort["label"],
            "patientId": row["patientId"],
            "time_months": t,
            "event": int(event),
            "log10_ratio": math.log10(max(cls["N_e_ratio"], 0.01)),
            "above_threshold": cls["above_threshold"],
        })
    return pd.DataFrame(records)


def main() -> None:
    L_table = load_L_table()
    out_dir = ROOT / "data" / "ed_tcga"
    out_dir.mkdir(parents=True, exist_ok=True)

    frames = [build_cohort(c, L_table) for c in TCGA_COHORTS]
    df = pd.concat(frames, ignore_index=True)
    df.to_csv(out_dir / "tcga_pooled_patients.csv", index=False)

    summaries = []
    for label, sub in df.groupby("label"):
        above = sub[sub["above_threshold"]]
        below = sub[~sub["above_threshold"]]
        lr_p = float("nan")
        if len(above) >= 3 and len(below) >= 3:
            lr = logrank_test(above["time_months"], below["time_months"], above["event"], below["event"])
            lr_p = lr.p_value
        cph = CoxPHFitter()
        cph.fit(sub[["time_months", "event", "log10_ratio"]], "time_months", "event")
        s = cph.summary.loc["log10_ratio"]
        summaries.append({
            "cohort": label,
            "n": len(sub),
            "n_below": int((~sub["above_threshold"]).sum()),
            "pct_above": 100 * sub["above_threshold"].mean(),
            "logrank_p": lr_p,
            "cox_HR": float(s["exp(coef)"]),
            "cox_p": float(s["p"]),
        })

    pooled = {
        "cohort": "TCGA_pooled",
        "n": len(df),
        "n_below": int((~df["above_threshold"]).sum()),
        "pct_above": 100 * df["above_threshold"].mean(),
    }
    above = df[df["above_threshold"]]
    below = df[~df["above_threshold"]]
    if len(above) >= 3 and len(below) >= 3:
        lr = logrank_test(above["time_months"], below["time_months"], above["event"], below["event"])
        pooled["logrank_p"] = lr.p_value
    cph = CoxPHFitter()
    cph.fit(df[["time_months", "event", "log10_ratio"]], "time_months", "event")
    s = cph.summary.loc["log10_ratio"]
    pooled["cox_HR"] = float(s["exp(coef)"])
    pooled["cox_p"] = float(s["p"])
    summaries.append(pooled)

    summary_df = pd.DataFrame(summaries)
    summary_df.to_csv(out_dir / "km_cox_summary.csv", index=False)

    fig, ax = plt.subplots(figsize=(NATURE_2COL, NATURE_2COL * 0.62))
    for sub, lbl, c in [(above, r"$N_e \geq N_e^*$", "#D6604D"), (below, r"$N_e < N_e^*$", "#2166AC")]:
        KaplanMeierFitter().fit(sub["time_months"], sub["event"], label=f"{lbl} (n={len(sub)})").plot(
            ax=ax, ci_show=True, color=c, linewidth=2,
        )
    ax.set_xlabel("Progression-free survival (months)", fontsize=10)
    ax.set_ylabel("Survival probability", fontsize=10)
    ax.tick_params(labelsize=9)
    ax.legend(fontsize=9, loc="lower left", framealpha=0.9)
    lr_p = pooled.get("logrank_p", float("nan"))
    ax.set_title(
        f"Extended Data: TCGA generic PFS (n = {len(df)}, log-rank P = {lr_p:.3g})",
        loc="left", fontsize=10, pad=12,
    )
    fig.tight_layout(pad=1.2)
    fig.savefig(out_dir / "ed_tcga_pfs_km.pdf", dpi=300)
    fig.savefig(out_dir / "ed_tcga_pfs_km.png", dpi=300)
    plt.close()

    print(summary_df.to_string(index=False))
    print(f"Wrote {out_dir}")


if __name__ == "__main__":
    main()
