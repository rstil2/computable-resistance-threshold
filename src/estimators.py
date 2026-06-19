"""
Patient-level estimators for V_A, h², and N_e from sequencing data.
Independent of outcome endpoints and of L.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence

import numpy as np


@dataclass
class MutationRecord:
    vaf: float
    is_synonymous: bool = False


def math_score(vafs: Sequence[float]) -> float:
    """
    MATH score proxy for V_A: 100 * MAD(VAF) / median(VAF).
    Mroz & Rocco 2013.
    """
    v = np.asarray(vafs, dtype=float)
    v = v[(v > 0) & (v < 1)]
    if len(v) < 3:
        return float("nan")
    med = np.median(v)
    if med <= 0:
        return float("nan")
    mad = np.median(np.abs(v - med))
    return 100.0 * mad / med


def subclonal_fraction(vafs: Sequence[float], clonal_threshold: float = 0.20) -> float:
    """ITH / h² proxy: fraction of mutations below clonal VAF threshold."""
    v = np.asarray(vafs, dtype=float)
    v = v[(v > 0) & (v < 1)]
    if len(v) == 0:
        return float("nan")
    return float(np.mean(v < clonal_threshold))


def va_from_vafs(vafs: Sequence[float], method: str = "math") -> float:
    """V_A proxy from per-sample VAF list."""
    if method == "math":
        score = math_score(vafs)
        if np.isnan(score):
            return float("nan")
        # Calibrate MATH → V_A scale (PCAWG median ≈ 0.08 at MATH≈15)
        return max(score / 180.0, 1e-4)
    if method == "variance":
        v = np.asarray(vafs, dtype=float)
        v = v[(v > 0) & (v < 1)]
        return float(np.var(v)) if len(v) >= 2 else float("nan")
    raise ValueError(f"Unknown V_A method: {method}")


def ne_from_vaf_spectrum(
    vafs: Sequence[float],
    *,
    mu_eff: float = 1e-9,
    t_div: float = 30.0,
    f_min: float = 0.05,
) -> float:
    """
    Williams et al. 2016 style N_e from subclonal VAF site-frequency spectrum.

    Uses subclonal mutation count and median VAF to estimate effective population
    size on the same scale as published TCGA/PCAWG values (~10³–10⁴), not census
    cell counts. Calibrated so typical resected tumours fall near Williams medians.
    """
    v = np.asarray(vafs, dtype=float)
    v = v[(v >= f_min) & (v <= 0.5)]
    if len(v) < 5:
        return float("nan")

    med = float(np.median(v))
    if med <= 0:
        return float("nan")

    # Clone-size / drift proxy: more subclonal mutations at lower median VAF
    # implies larger effective population under neutral drift scaling.
    # sqrt(n) / median(VAF) is monotone in Ne on published scales.
    Ne = (np.sqrt(len(v)) / med) * 800.0
    return max(float(Ne), 10.0)


def ne_from_cellularity(
    tumor_purity: float,
    estimated_cells: float = 1e9,
) -> float:
    """Secondary N_e: purity × absolute cell burden at sequencing."""
    if tumor_purity <= 0 or tumor_purity > 1:
        return float("nan")
    return max(tumor_purity * estimated_cells, 10.0)


def estimate_patient_metrics(
    vafs: Sequence[float],
    *,
    tumor_purity: Optional[float] = None,
    clonal_threshold: float = 0.20,
    calibrated_ne: Optional[float] = None,
) -> dict:
    """Compute all patient-level inputs except L (from driver table)."""
    raw_ne = ne_from_vaf_spectrum(vafs)
    out = {
        "V_A_math": va_from_vafs(vafs, method="math"),
        "V_A_var": va_from_vafs(vafs, method="variance"),
        "h2_proxy": subclonal_fraction(vafs, clonal_threshold),
        "MATH": math_score(vafs),
        "N_e_sfs_raw": raw_ne,
        "N_e_sfs": calibrated_ne if calibrated_ne is not None else raw_ne,
        "n_mutations": len(vafs),
    }
    if tumor_purity is not None:
        out["N_e_cellularity"] = ne_from_cellularity(tumor_purity)
    return out
