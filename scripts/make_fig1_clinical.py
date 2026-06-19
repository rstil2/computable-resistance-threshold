#!/usr/bin/env python3
"""Fig 1: N_e* concept mapped onto a mock clinical sequencing report."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from threshold import ne_star, pac_bound  # noqa: E402

FIG_W = 7.5
FIG_H = 5.0

# Panel interior layout (axes coords 0–1)
CARD = dict(x=0.06, y=0.08, w=0.88, h=0.80)
ROW_X_LABEL = 0.11
ROW_X_VALUE = 0.88
ROW_H = 0.072


def _row_band(ax, y_center: float, highlight: bool = False) -> None:
    """Background band for one table row; text is drawn on top (zorder 3)."""
    y0 = y_center - ROW_H / 2
    if highlight:
        ax.add_patch(mpatches.Rectangle(
            (CARD["x"] + 0.02, y0), 0.50, ROW_H,
            fc="#EBF5FB", ec="#2166AC", lw=1.0, ls="--",
            zorder=1, clip_on=True,
        ))


def _row_text(ax, y_center: float, label: str, value: str | None = None) -> None:
    ax.text(
        ROW_X_LABEL, y_center, label,
        fontsize=10, va="center", ha="left", color="0.25", zorder=3, clip_on=True,
    )
    if value is not None:
        ax.text(
            ROW_X_VALUE, y_center, value,
            fontsize=10, va="center", ha="right", family="monospace", color="0.05",
            zorder=3, clip_on=True,
        )


def draw_report_panel(ax, *, VA: float, Ne: float, L: int) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_clip_on(True)

    ax.add_patch(mpatches.FancyBboxPatch(
        (CARD["x"], CARD["y"]), CARD["w"], CARD["h"],
        boxstyle="round,pad=0.012", fc="white", ec="#BBBBBB", lw=1.0, zorder=0,
    ))

    ax.text(
        CARD["x"] + 0.04, CARD["y"] + CARD["h"] - 0.06,
        "TUMOUR SEQUENCING SUMMARY",
        fontsize=11, fontweight="bold", va="top", ha="left", zorder=3,
    )
    ax.text(
        CARD["x"] + 0.04, CARD["y"] + CARD["h"] - 0.12,
        "Melanoma (SKCM)  ·  Patient ID redacted",
        fontsize=9.5, va="top", ha="left", color="0.45", zorder=3,
    )

    rows = [
        ("section", 0.68, "Intratumour heterogeneity", None, False),
        ("row", 0.60, "Subclonal fraction (h²)", "0.62", False),
        ("row", 0.52, "CCF variance (V_A)", f"{VA:.3f}", True),
        ("section", 0.42, "Effective population size", None, False),
        ("row", 0.34, "N_e (VAF spectrum)", f"{Ne:,.0f} cells", True),
        ("row", 0.24, "Resistance loci (L)", f"{L} loci", True),
        ("section", 0.14, "Actionable variants", None, False),
        ("row", 0.10, "BRAF p.V600E (clonal)", "12.4 mut/Mb", False),
    ]

    for kind, y, label, value, hi in rows:
        if kind == "section":
            ax.text(
                ROW_X_LABEL, y, label,
                fontsize=10.5, fontweight="bold", va="center", ha="left",
                color="0.12", zorder=3, clip_on=True,
            )
        else:
            _row_band(ax, y, highlight=hi)
            _row_text(ax, y, label, value)


def draw_threshold_panel(ax, *, Ne: float, nstar: float, eps: float) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_clip_on(True)

    # Outer panel frame so footer/formula text is not visually orphaned
    ax.add_patch(mpatches.FancyBboxPatch(
        (0.05, 0.03), 0.90, 0.90,
        boxstyle="round,pad=0.012", fc="white", ec="#BBBBBB", lw=1.0, zorder=0,
    ))

    above = Ne >= nstar
    status = "ABOVE N_e*\nresistance learnable" if above else "BELOW N_e*\nresistance precluded"
    accent = "#D6604D" if above else "#2166AC"

    # Result card — evenly spaced lines inside box (no y collisions)
    bx, by, bw, bh = 0.10, 0.30, 0.80, 0.54
    ax.add_patch(mpatches.FancyBboxPatch(
        (bx, by), bw, bh,
        boxstyle="round,pad=0.015", fc="#F7FAFC", ec=accent, lw=2.0, zorder=1,
    ))

    cx = bx + bw / 2
    y_top = by + bh - 0.12
    y_bot = by + 0.14
    step = (y_top - y_bot) / 4
    ys = [y_top - i * step for i in range(5)]

    texts = [
        (r"$N_e^*$ threshold", 11, "bold", "0.2"),
        (rf"$N_e^* = {nstar:,.0f}$ cells", 13, "bold", "0.05"),
        (rf"$\varepsilon^* = {eps:.3f}$", 11, "normal", "0.15"),
        (rf"Patient $N_e / N_e^* = {Ne / nstar:.2f}$", 11, "normal", "0.15"),
        (status, 9.5, "bold", accent),
    ]
    for y, (txt, fs, weight, color) in zip(ys, texts):
        ax.text(
            cx, y, txt, ha="center", va="center",
            fontsize=fs, fontweight=weight, color=color, zorder=3, clip_on=True,
            linespacing=1.25,
        )

    ax.text(
        cx, by + bh + 0.05,
        "Computed from  V_A ,  N_e ,  L",
        ha="center", va="bottom", fontsize=9.5, color=accent, zorder=3, clip_on=True,
    )

    ax.text(
        cx, 0.16,
        r"$N_e^* = \min\{N_e : P(\mathrm{failure}) \leq \delta\}$"
        "\n" r"$\varepsilon = 0.05$,  $\delta = 0.05$",
        ha="center", va="center", fontsize=9, color="0.40", zorder=3, linespacing=1.4,
        clip_on=True,
    )
    ax.text(
        cx, 0.04,
        "Clinical goal: keep N_e below N_e*",
        ha="center", va="center", fontsize=9, color="0.38", style="italic", zorder=3,
        clip_on=True,
    )


def add_panel_title(fig, ax, letter: str, title: str) -> None:
    """Place A/B titles in figure coordinates above each axes — avoids axis-edge clipping."""
    pos = ax.get_position()
    fig.text(
        pos.x0, pos.y1 + 0.015, letter,
        fontsize=14, fontweight="bold", va="bottom", ha="left",
    )
    fig.text(
        pos.x0 + 0.025, pos.y1 + 0.015, title,
        fontsize=11, fontweight="bold", va="bottom", ha="left",
    )


def main() -> None:
    VA, L, Ne = 0.14, 10, 8200.0
    nstar = ne_star(VA, L)
    eps = pac_bound(Ne, VA, L)

    out_dir = ROOT / "data" / "fig1"
    out_dir.mkdir(parents=True, exist_ok=True)

    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })

    fig = plt.figure(figsize=(FIG_W, FIG_H), facecolor="white")
    gs = GridSpec(1, 2, figure=fig, width_ratios=[1.05, 0.95], wspace=0.22)

    ax_left = fig.add_subplot(gs[0])
    ax_right = fig.add_subplot(gs[1])

    draw_report_panel(ax_left, VA=VA, Ne=Ne, L=L)
    draw_threshold_panel(ax_right, Ne=Ne, nstar=nstar, eps=eps)

    fig.subplots_adjust(left=0.06, right=0.96, top=0.86, bottom=0.12, wspace=0.24)
    add_panel_title(fig, ax_left, "A", "Standard tumour sequencing report")
    add_panel_title(fig, ax_right, "B", "Resistance-learnability threshold")

    for ext in ("pdf", "png"):
        fig.savefig(
            out_dir / f"fig1_clinical_report.{ext}",
            dpi=300,
            facecolor="white",
            edgecolor="none",
            pad_inches=0.12,
        )
    plt.close()
    print(f"Wrote {out_dir / 'fig1_clinical_report.pdf'}")


if __name__ == "__main__":
    main()
