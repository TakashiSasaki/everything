#!/usr/bin/env python3
"""
Ensure each function heading has a stable HTML anchor.

For every H2 heading matching '## Everything_*', insert (if missing)
HTML anchors with both underscore and hyphen forms, e.g.:

  ## Everything_CleanUp
  <a id="everything_cleanup"></a>
  <a id="everything-cleanup"></a>

This makes in-document links robust across markdown renderers that
disagree on slug rules.

Usage:
  python tools/add_heading_anchors.py reference.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List


HEAD_RE = re.compile(r"^##\s+(Everything_[A-Za-z0-9_]+)\s*$")


def underscore_slug(name: str) -> str:
    return name.strip().lower().replace(" ", "-")


def hyphen_slug(name: str) -> str:
    return underscore_slug(name).replace("_", "-")


def ensure_anchors(md: str) -> str:
    lines = md.splitlines()
    out: List[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        m = HEAD_RE.match(line)
        if m:
            name = m.group(1)
            u = underscore_slug(name)
            h = hyphen_slug(name)
            # Look ahead to see if anchors already present
            j = i + 1
            have_u = False
            have_h = False
            while j < len(lines) and lines[j].strip().startswith("<a "):
                tag = lines[j].strip()
                if f'id="{u}"' in tag:
                    have_u = True
                if f'id="{h}"' in tag:
                    have_h = True
                out.append(lines[j])
                j += 1
            # Insert missing anchors
            if not have_u:
                out.append(f"<a id=\"{u}\"></a>")
            if not have_h and h != u:
                out.append(f"<a id=\"{h}\"></a>")
            # Continue from where we looked ahead
            i = j
            continue
        i += 1
    return "\n".join(out) + ("\n" if md.endswith("\n") else "")


def main(argv: List[str]) -> int:
    if len(argv) != 2:
        print("Usage: python tools/add_heading_anchors.py <markdown-file>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    text = path.read_text(encoding="utf-8")
    new_text = ensure_anchors(text)
    path.write_text(new_text, encoding="utf-8")
    print(f"Anchors ensured in {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

