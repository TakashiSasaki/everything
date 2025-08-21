#!/usr/bin/env python3
"""
Auto-link function names in markdown to their in-document anchors.

Targets tokens like `Everything_*` and links them to `#everything_*`
when a corresponding H2 heading `## Everything_*` exists in the document.

Preserves code blocks and inline code, and avoids modifying existing
markdown links by not touching text inside square brackets.

Usage:
  python tools/autolink_functions.py reference.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, List


HEADING_RE = re.compile(r"^##\s+(Everything_[A-Za-z0-9_]+)\s*$")
TOKEN_RE = re.compile(r"\b(Everything_[A-Za-z0-9_]+)\b")


def slugify(h: str) -> str:
    return re.sub(r"[^a-z0-9_-]", "", h.strip().lower().replace(" ", "-"))


def build_anchor_map(lines: List[str]) -> Dict[str, str]:
    anchors: Dict[str, str] = {}
    for line in lines:
        m = HEADING_RE.match(line)
        if m:
            name = m.group(1)
            anchors[name] = slugify(name)
    return anchors


def transform_line(line: str, anchors: Dict[str, str]) -> str:
    # Respect fenced code blocks handled by caller; here we only handle inline code with backticks
    parts = line.split("`")
    for i in range(0, len(parts), 2):  # even indices: outside inline code
        segment = parts[i]
        # Protect text inside square brackets (likely link text): we won't modify inside [ ... ]
        out_segment = []
        buf = []
        depth = 0
        for ch in segment:
            if ch == '[':
                # flush current modifiable buffer
                if buf:
                    s = ''.join(buf)
                    s = TOKEN_RE.sub(lambda m: f"[{m.group(1)}](#{anchors[m.group(1)]})" if m.group(1) in anchors else m.group(0), s)
                    out_segment.append(s)
                    buf = []
                depth += 1
                out_segment.append(ch)
            elif ch == ']':
                depth = max(0, depth - 1)
                out_segment.append(ch)
            else:
                if depth == 0:
                    buf.append(ch)
                else:
                    out_segment.append(ch)
        # flush tail
        if buf:
            s = ''.join(buf)
            s = TOKEN_RE.sub(lambda m: f"[{m.group(1)}](#{anchors[m.group(1)]})" if m.group(1) in anchors else m.group(0), s)
            out_segment.append(s)
        parts[i] = ''.join(out_segment)
    return '`'.join(parts)


def autolink(text: str) -> str:
    lines = text.splitlines()
    anchors = build_anchor_map(lines)

    out: List[str] = []
    in_fence = False
    for line in lines:
        # Detect fenced code blocks (```) start/end
        if line.strip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        out.append(transform_line(line, anchors))
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def main(argv: List[str]) -> int:
    if len(argv) != 2:
        print("Usage: python tools/autolink_functions.py <markdown-file>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    text = path.read_text(encoding="utf-8")
    new_text = autolink(text)
    path.write_text(new_text, encoding="utf-8")
    print(f"Auto-linked functions in {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

