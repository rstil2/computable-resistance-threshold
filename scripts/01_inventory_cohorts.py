#!/usr/bin/env python3
"""Inventory configured cBioPortal cohorts and write eligibility report."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cbioportal import cohort_summary, fetch_patient_table  # noqa: E402


def endpoint_coverage(study_id: str, fields: list[str]) -> dict:
    rows = fetch_patient_table(study_id)
    cov = {}
    for field in fields:
        nonmiss = sum(1 for r in rows if str(r.get(field, "")).strip() not in ("", "NA", "Unknown"))
        cov[field] = {"non_missing": nonmiss, "fraction": round(nonmiss / max(len(rows), 1), 3)}
    return cov


def main() -> None:
    cfg = yaml.safe_load(open(ROOT / "config" / "cohorts.yaml"))
    report = {"primary": [], "replication": [], "bonus": []}

    for tier in ("primary", "replication"):
        for cohort in cfg.get(tier, []):
            sid = cohort["study_id"]
            print(f"Scanning {sid} …")
            summary = cohort_summary(sid)
            fields = [cohort.get("endpoint_field"), cohort.get("endpoint_status")]
            fields = [f for f in fields if f]
            summary["endpoint_coverage"] = endpoint_coverage(sid, fields) if fields else {}
            summary["config"] = cohort
            report[tier].append(summary)

    report["bonus"] = cfg.get("bonus", [])
    out = ROOT / "data" / "cohort_inventory.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as fh:
        json.dump(report, fh, indent=2)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
