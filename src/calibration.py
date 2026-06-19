"""Calibrate patient-level N_e to Williams et al. 2016 reference scale."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

_CONFIG = Path(__file__).resolve().parent.parent / "config" / "williams_Ne_reference.tsv"


def load_ne_reference(path: Optional[Path] = None) -> Dict[str, float]:
    table: Dict[str, float] = {}
    with open(path or _CONFIG) as fh:
        for line in fh:
            if line.startswith("#") or line.startswith("cancer_type"):
                continue
            parts = line.strip().split("\t")
            if len(parts) >= 2:
                table[parts[0]] = float(parts[1])
    return table


def calibrate_ne(raw_ne: float, cohort_median_raw: float, cancer_type: str) -> float:
    """
    Scale raw N_e so the cohort median matches Williams reference for cancer_type.
    Preserves rank order within cohort.
    """
    ref = load_ne_reference().get(cancer_type, load_ne_reference().get("DEFAULT", 5000.0))
    if cohort_median_raw <= 0 or raw_ne != raw_ne:
        return float("nan")
    return max(raw_ne * (ref / cohort_median_raw), 10.0)
