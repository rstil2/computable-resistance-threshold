#!/usr/bin/env python3
"""Head-to-head benchmark: ε* vs V_A (MATH) and N_e alone on cross-cancer ecology."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

OUT_DIR = ROOT / "data" / "fig2_cross_cancer"


def ols_r2(y: np.ndarray, X: np.ndarray) -> float:
    X = np.column_stack([np.ones(len(y)), X])
    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    ss_res = float(np.sum(resid**2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")


def nested_f_p(y: np.ndarray, X_base: np.ndarray, X_full: np.ndarray) -> float:
    """F-test p-value for extra columns in X_full vs X_base."""
    n = len(y)
    k_base = X_base.shape[1] + 1
    k_full = X_full.shape[1] + 1
    r2_base = ols_r2(y, X_base)
    r2_full = ols_r2(y, X_full)
    df_num = k_full - k_base
    df_den = n - k_full - 1
    if df_den <= 0 or r2_full <= r2_base:
        return 1.0
    f = ((r2_full - r2_base) / df_num) / ((1 - r2_full) / df_den)
    return float(stats.f.sf(f, df_num, df_den))


def loo_min_r(x: np.ndarray, y: np.ndarray) -> float:
    rs = []
    for i in range(len(y)):
        mask = np.ones(len(y), dtype=bool)
        mask[i] = False
        rs.append(stats.pearsonr(x[mask], y[mask]).statistic)
    return float(min(rs))


def main() -> None:
    df = pd.read_csv(OUT_DIR / "cross_cancer_table.csv")
    y = df["gen_err"].values
    va = df["VA"].values
    logne = np.log10(df["Ne"].values)
    inv_ne = 1.0 / df["Ne"].values
    eps = df["eps_star"].values
    L = df["L"].values.astype(float)

    rows = []
    for label, x in [
        ("V_A (MATH-calibrated)", va),
        ("log10(N_e)", logne),
        ("1/N_e", inv_ne),
        ("epsilon_star (PAC bound)", eps),
    ]:
        r, p = stats.pearsonr(x, y)
        rows.append({
            "predictor": label,
            "pearson_r": round(float(r), 3),
            "pearson_p": float(p),
            "loo_r_min": round(loo_min_r(x, y), 3),
            "ols_r2": round(ols_r2(y, x.reshape(-1, 1) if x.ndim == 1 else x), 3),
        })

    for label, X in [
        ("V_A + log10(N_e)", np.column_stack([va, logne])),
        ("V_A + log10(N_e) + L", np.column_stack([va, logne, L])),
    ]:
        rows.append({
            "predictor": label,
            "pearson_r": None,
            "pearson_p": None,
            "loo_r_min": None,
            "ols_r2": round(ols_r2(y, X), 3),
        })

    out = pd.DataFrame(rows)
    out.to_csv(OUT_DIR / "benchmark_metrics.csv", index=False)

    X_base = np.column_stack([va, logne])
    X_full = np.column_stack([va, logne, eps])
    nested = {
        "base_r2": round(ols_r2(y, X_base), 3),
        "with_eps_r2": round(ols_r2(y, X_full), 3),
        "delta_r2": round(ols_r2(y, X_full) - ols_r2(y, X_base), 4),
        "nested_f_p": round(nested_f_p(y, X_base, X_full), 3),
    }
    pd.DataFrame([nested]).to_csv(OUT_DIR / "benchmark_nested.csv", index=False)

    print("Benchmark metrics:")
    print(out.to_string(index=False))
    print("\nNested model (V_A + log10 N_e vs + ε*):", nested)


if __name__ == "__main__":
    main()
