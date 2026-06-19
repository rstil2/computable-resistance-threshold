#!/usr/bin/env python3
"""
Fig 2 primary analysis: patient-level N_e vs N_e* → Kaplan–Meier.

OSF locked 2026-06-19. Uses real mutation VAFs from cBioPortal.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cbioportal import fetch_patient_table, patient_vaf_map, parse_purity  # noqa: E402
from estimators import estimate_patient_metrics  # noqa: E402
from threshold import classify_patient, load_L_table  # noqa: E402

try:
    from lifelines import KaplanMeierFitter
    from lifelines.statistics import logrank_test
except ImportError as exc:
    raise SystemExit("Install lifelines: pip install lifelines") from exc


def parse_endpoint(row: dict, cohort: dict) -> tuple[float, bool]:
    field = cohort["endpoint_field"]
    raw = row.get(field, "")
    if not raw:
        return float("nan"), False

    t = float(raw)
    if field == "DURATION_OF_THERAPY_WEEKS":
        t *= 12.0 / 52.0

    event = True
    status = cohort.get("endpoint_status")
    if status:
        val = row.get(status, "")
        event = "Progressed" in val or "1:" in val or val in ("DECEASED", "1:DECEASED")
    if cohort.get("endpoint_event"):
        if row.get("EARLY_RESISTANCE") == "Yes":
            event = True
        if row.get("TREATMENT_BEST_RESPONSE") == "PD":
            event = True
    return t, event


def metrics_eligible(metrics: dict) -> bool:
    """Pre-registered genomic quality gates."""
    import math

    if metrics.get("n_mutations", 0) < 3:
        return False
    if math.isnan(metrics.get("V_A_math", float("nan"))):
        return False
    if math.isnan(metrics.get("N_e_sfs", float("nan"))):
        return False
    return True


def run_cohort(cohort: dict, L_table: dict, vafs: dict[str, list[float]]) -> pd.DataFrame:
    study_id = cohort["study_id"]
    cancer_type = cohort["cancer_type"]
    L = L_table.get(cancer_type, L_table.get("DEFAULT", 12))

    rows = fetch_patient_table(study_id)
    records = []
    skipped = {"no_outcome": 0, "no_vafs": 0, "quality": 0}

    for row in rows:
        pid = row["patientId"]
        time_m, event = parse_endpoint(row, cohort)
        if pd.isna(time_m):
            skipped["no_outcome"] += 1
            continue

        patient_vafs = vafs.get(pid)
        if not patient_vafs:
            skipped["no_vafs"] += 1
            continue

        purity = parse_purity(row)
        metrics = estimate_patient_metrics(patient_vafs, tumor_purity=purity)
        if not metrics_eligible(metrics):
            skipped["quality"] += 1
            continue

        cls = classify_patient(metrics["N_e_sfs"], metrics["V_A_math"], L)

        records.append({
            "study_id": study_id,
            "patientId": pid,
            "time_months": time_m,
            "event": event,
            "above_threshold": cls["above_threshold"],
            "N_e": cls["N_e"],
            "N_e_star": cls["N_e_star"],
            "N_e_ratio": cls["N_e_ratio"],
            "V_A": cls["V_A"],
            "h2_proxy": metrics["h2_proxy"],
            "MATH": metrics["MATH"],
            "n_mutations": metrics["n_mutations"],
            "L": L,
        })

    print(f"    eligible={len(records)}  skipped={skipped}")
    return pd.DataFrame(records)


def km_plot(df: pd.DataFrame, out_path: Path, title: str) -> dict:
    above = df[df["above_threshold"]]
    below = df[~df["above_threshold"]]

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(5, 4))
    if len(above) >= 1:
        KaplanMeierFitter().fit(
            above["time_months"], above["event"], label=f"N_e ≥ N_e* (n={len(above)})"
        ).plot(ax=ax, ci_show=True)
    if len(below) >= 1:
        KaplanMeierFitter().fit(
            below["time_months"], below["event"], label=f"N_e < N_e* (n={len(below)})"
        ).plot(ax=ax, ci_show=True)

    ax.set_xlabel("Time (months)")
    ax.set_ylabel("Event-free survival")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close()

    if len(above) >= 5 and len(below) >= 5:
        lr = logrank_test(
            above["time_months"], below["time_months"],
            above["event"], below["event"],
        )
        return {
            "logrank_p": float(lr.p_value),
            "n_above": len(above),
            "n_below": len(below),
            "n_total": len(df),
        }
    return {
        "logrank_p": float("nan"),
        "n_above": len(above),
        "n_below": len(below),
        "n_total": len(df),
    }


def main() -> None:
    cfg = yaml.safe_load(open(ROOT / "config" / "cohorts.yaml"))
    L_table = load_L_table()
    out_dir = ROOT / "data" / "fig2"
    out_dir.mkdir(parents=True, exist_ok=True)

    all_stats = []
    all_patients = []

    for cohort in cfg["primary"]:
        sid = cohort["study_id"]
        print(f"\n=== {sid} ===")
        print("  Fetching VAFs …")
        vafs = patient_vaf_map(sid)
        print(f"  Patients with VAF data: {len(vafs)}")

        df = run_cohort(cohort, L_table, vafs)
        df.to_csv(out_dir / f"{sid}_patients.csv", index=False)
        all_patients.append(df)

        if len(df) >= 10:
            stats = km_plot(df, out_dir / f"{sid}_km.pdf", title=sid)
            stats["study_id"] = sid
            all_stats.append(stats)
            print(f"  KM: n={stats['n_total']}  above={stats['n_above']}  below={stats['n_below']}  p={stats['logrank_p']:.4g}")
        else:
            print(f"  Too few eligible patients (n={len(df)}) for KM")

    # Pooled TCGA (pre-registered if heterogeneity allows — report pooled + per-cohort)
    tcga_ids = {
        "luad_tcga_pan_can_atlas_2018",
        "skcm_tcga_pan_can_atlas_2018",
        "coadread_tcga_pan_can_atlas_2018",
    }
    pooled = pd.concat([d for d in all_patients if not d.empty and d["study_id"].iloc[0] in tcga_ids], ignore_index=True)
    if len(pooled) >= 20:
        stats = km_plot(pooled, out_dir / "tcga_pooled_km.pdf", title="TCGA pooled (LUAD+SKCM+COADREAD)")
        stats["study_id"] = "tcga_pooled"
        all_stats.append(stats)
        print(f"\n=== TCGA pooled ===")
        print(f"  n={stats['n_total']}  above={stats['n_above']}  below={stats['n_below']}  p={stats['logrank_p']:.4g}")
        pooled.to_csv(out_dir / "tcga_pooled_patients.csv", index=False)

    pd.DataFrame(all_stats).to_csv(out_dir / "km_summary.csv", index=False)
    print(f"\nDone. Outputs → {out_dir}")


if __name__ == "__main__":
    main()
