#!/usr/bin/env python3
"""Run all five Nat Cancer strengthening analyses (Figs 1–4)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = ROOT / ".venv" / "bin" / "python"
SCRIPTS = [
    "make_fig1_clinical.py",
    "make_fig2_cross_cancer.py",
    "make_fig3_targeted.py",
    "make_fig4_utility.py",
    "make_ed_tcga_null.py",
]
POST_SCRIPTS = ["build_supplementary_note_1.py", "build_manuscript_docx.py"]


def main() -> None:
    env = {"MPLCONFIGDIR": str(ROOT / ".mpl")}
    for name in SCRIPTS:
        path = ROOT / "scripts" / name
        print(f"\n{'='*60}\n>>> {name}\n{'='*60}")
        r = subprocess.run([str(PY), str(path)], cwd=str(ROOT), env={**dict(**__import__("os").environ), **env})
        if r.returncode != 0:
            sys.exit(r.returncode)
    for name in POST_SCRIPTS:
        path = ROOT / "scripts" / name
        print(f"\n{'='*60}\n>>> {name}\n{'='*60}")
        r = subprocess.run([str(PY), str(path)], cwd=str(ROOT), env={**dict(**__import__("os").environ), **env})
        if r.returncode != 0:
            sys.exit(r.returncode)
    print("\nAll figures complete.")


if __name__ == "__main__":
    main()
