#!/usr/bin/env python3
"""Export manuscript/content.py to readable Markdown."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "manuscript"))

from content import (  # noqa: E402
    ABSTRACT,
    ACKNOWLEDGEMENTS,
    AFFILIATION,
    AUTHOR_CONTRIBUTIONS,
    AUTHORS,
    COMPETING_INTERESTS,
    CORRESPONDING,
    DATA_AVAILABILITY,
    DISCUSSION,
    ETHICS,
    EXTENDED_DATA_TABLES,
    GITHUB_REPO,
    INTRODUCTION,
    KEY_POINTS,
    KEYWORDS,
    METHODS,
    REFERENCES,
    RESULTS,
    TITLE,
)

OUT = ROOT / "docs" / "MANUSCRIPT_full.md"


def render_blocks(blocks: list) -> list[str]:
    lines: list[str] = []
    for block in blocks:
        if block[0] == "heading2":
            lines.append(f"\n### {block[1]}\n")
        elif block[0] == "para":
            lines.append(block[1] + "\n")
        elif block[0] == "figure":
            _, label, legend = block
            lines.append(f"\n*{label}. {legend.replace('**', '*')}*\n")
    return lines


def main() -> None:
    parts = [
        f"# {TITLE}\n",
        f"**{AUTHORS}**  \n*{AFFILIATION}*  \n{CORRESPONDING}\n",
        "## Abstract\n",
        *[p + "\n" for p in ABSTRACT],
        f"**Keywords:** {KEYWORDS}\n",
        "## Key points\n",
        *[f"- {k}\n" for k in KEY_POINTS],
        "## Introduction\n",
        *[p + "\n" for p in INTRODUCTION],
        "## Results\n",
        *render_blocks(RESULTS),
        "## Discussion\n",
        *[p + "\n" for p in DISCUSSION],
        "## Methods\n",
        *render_blocks(METHODS),
        "## Extended Data\n",
    ]
    for title, sub, body in EXTENDED_DATA_TABLES:
        parts.append(f"### {title}\n*{sub}*\n\n{body}\n\n")
    parts.extend([
        "## Data availability\n", DATA_AVAILABILITY + "\n",
        "## Ethics statement\n", ETHICS + "\n",
        "## Acknowledgements\n", ACKNOWLEDGEMENTS + "\n",
        "## Author contributions\n", AUTHOR_CONTRIBUTIONS + "\n",
        "## Competing interests\n", COMPETING_INTERESTS + "\n",
        "## References\n",
        *[f"{i}. {r}\n" for i, r in enumerate(REFERENCES, 1)],
    ])
    OUT.write_text("".join(parts))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
