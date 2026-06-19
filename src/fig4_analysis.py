"""
Fig 4 analysis: resistance emergence vs manipulated N_e / N_e*.

Works on real lab data (CSV) or simulation output with identical schema.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy import stats


@dataclass
class ChangepointResult:
    slope_below: float
    slope_above: float
    intercept: float
    changepoint_log10: float
    aic_single: float
    aic_piecewise: float
    p_chow: float


def logit(p: np.ndarray) -> np.ndarray:
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return np.log(p / (1 - p))


def fit_primary_logistic(df: pd.DataFrame) -> Dict[str, float]:
    """
    Primary: resistance ~ log10(N_e / N_e_star).
    Uses statsmodels if available, else closed-form-ish GLM via scipy.
    """
    x = np.log10(df["N_e"] / df["N_e_star"])
    y = df["resistance"].astype(float)

    # Design matrix with intercept
    X = np.column_stack([np.ones(len(x)), x])
    # IRLS for logistic
    beta = np.zeros(2)
    for _ in range(25):
        eta = X @ beta
        p = 1 / (1 + np.exp(-eta))
        w = p * (1 - p) + 1e-9
        z = eta + (y - p) / w
        xt_w = X.T * w
        beta = np.linalg.lstsq(xt_w @ X, xt_w @ z, rcond=None)[0]
    eta = X @ beta
    p = 1 / (1 + np.exp(-eta))
    # Wald SE
    w = p * (1 - p) + 1e-9
    xt_w = X.T * w
    cov = np.linalg.inv(xt_w @ X)
    se = np.sqrt(np.diag(cov))
    z = beta[1] / se[1]
    pval = 2 * (1 - stats.norm.cdf(abs(z)))

    return {
        "intercept": float(beta[0]),
        "coef_log10_ratio": float(beta[1]),
        "se_log10_ratio": float(se[1]),
        "p_log10_ratio": float(pval),
        "odds_ratio_per_log10": float(math.exp(beta[1])),
    }


def fit_changepoint_logistic(
    df: pd.DataFrame,
    cp_log10: float = 0.0,
) -> ChangepointResult:
    """Piecewise logistic with changepoint at log10(N_e/N_e*) = cp_log10."""
    x = np.log10(df["N_e"] / df["N_e_star"]).values
    y = df["resistance"].astype(float).values

    def nll(beta: np.ndarray) -> float:
        b0, b1, b2 = beta
        eta = np.where(
            x <= cp_log10,
            b0 + b1 * (x - cp_log10),
            b0 + b2 * (x - cp_log10),
        )
        p = 1 / (1 + np.exp(-np.clip(eta, -30, 30)))
        return -np.sum(y * np.log(p + 1e-12) + (1 - y) * np.log(1 - p + 1e-12))

    # Single slope model
    single = fit_primary_logistic(df)
    k = len(y)
    aic_single = 2 * 2 - 2 * (-nll(np.array([single["intercept"], single["coef_log10_ratio"], single["coef_log10_ratio"]])))

    from scipy.optimize import minimize

    res = minimize(
        nll,
        x0=np.array([0.0, 0.5, 2.0]),
        method="L-BFGS-B",
    )
    b0, b1, b2 = res.x
    aic_piecewise = 2 * 3 - 2 * (-res.fun)

    # Chow-style: LR test 1 df (nested if b1=b2)
    lr = 2 * (-res.fun - (-nll(np.array([single["intercept"], single["coef_log10_ratio"], single["coef_log10_ratio"]]))))
    p_chow = 1 - stats.chi2.cdf(max(lr, 0), df=1)

    return ChangepointResult(
        slope_below=float(b1),
        slope_above=float(b2),
        intercept=float(b0),
        changepoint_log10=cp_log10,
        aic_single=float(aic_single),
        aic_piecewise=float(aic_piecewise),
        p_chow=float(p_chow),
    )


def summarize_by_arm(df: pd.DataFrame) -> pd.DataFrame:
    """Fraction resistant per arm fraction."""
    g = df.groupby("arm_fraction", as_index=False).agg(
        n=("resistance", "size"),
        n_resistant=("resistance", "sum"),
        N_e_mean=("N_e", "mean"),
        ratio_mean=("N_e_ratio", "mean"),
    )
    g["p_resistance"] = g["n_resistant"] / g["n"]
    # Wilson CI
    z = 1.96
    phat = g["p_resistance"]
    n = g["n"]
    denom = 1 + z**2 / n
    centre = (phat + z**2 / (2 * n)) / denom
    half = z * np.sqrt((phat * (1 - phat) + z**2 / (4 * n)) / n) / denom
    g["ci_low"] = centre - half
    g["ci_high"] = centre + half
    return g
