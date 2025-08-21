#!/usr/bin/env python3
"""
Insert or update a Table of Contents in a markdown file.

Specifically targets Everything SDK reference where functions are listed
as H2 headings like '## Everything_*'. Generates links using GitHub-style
slugs: lowercase, spaces -> '-', remove characters other than [a-z0-9_-].

Usage:
  python tools/add_toc.py reference.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List


TOC_START = "<!-- TOC START -->"
TOC_END = "<!-- TOC END -->"


def slugify(h: str) -> str:
    s = h.strip().lower()
    s = s.replace(" ", "-")
    s = re.sub(r"[^a-z0-9_-]", "", s)
    return s


def build_toc(md: str) -> str:
    lines = md.splitlines()
    entries: List[str] = []
    for line in lines:
        if line.startswith("## "):
            title = line[3:].strip()
            # We only include actual function headings, not URL-derived ones
            if not title.startswith("Everything_"):
                continue
            anchor = slugify(title)
            entries.append(f"- [{title}](#{anchor})")

    toc_lines = [
        TOC_START,
        "## Table of Contents",
        *entries,
        TOC_END,
        "",
    ]
    return "\n".join(toc_lines)


def insert_toc(md: str) -> str:
    # Remove any existing TOC block
    md = re.sub(rf"{re.escape(TOC_START)}[\s\S]*?{re.escape(TOC_END)}\n?", "", md, flags=re.MULTILINE)

    # Find first H1 to place TOC after
    lines = md.splitlines()
    out: List[str] = []
    inserted = False
    for i, line in enumerate(lines):
        out.append(line)
        if not inserted and line.startswith("# "):
            out.append("")
            out.append(build_toc(md))
            inserted = True
    if not inserted:
        # If no H1, prepend
        return build_toc(md) + "\n" + md
    return "\n".join(out) + ("\n" if md.endswith("\n") else "\n")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python tools/add_toc.py <markdown-file>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    text = path.read_text(encoding="utf-8")
    new_text = insert_toc(text)
    path.write_text(new_text, encoding="utf-8")
    print(f"Updated TOC in {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

