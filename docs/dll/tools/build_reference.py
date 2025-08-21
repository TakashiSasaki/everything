#!/usr/bin/env python3
"""
Build a consolidated Everything SDK reference from a list of URLs.

Reads a Markdown file that contains a list of absolute URLs (one per line
or as bullet list items). Fetches each page, extracts the main content, and
writes a single `reference.md` with one section per function/page.

Designed to run locally on Windows (or any OS with network access).

Usage:
  python tools/build_reference.py --input docs/dll/draft.md --output docs/dll/reference.md

Notes:
- Extracts absolute URLs only; relative links are ignored (draft should contain absolutes).
- Heuristics try common content containers used on voidtools wiki pages.
- No external dependencies required beyond `requests` and `beautifulsoup4`.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import re
import sys
from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except Exception as e:  # pragma: no cover
    print("This script requires the 'requests' package.", file=sys.stderr)
    raise

try:
    from bs4 import BeautifulSoup, NavigableString, Tag  # type: ignore
except Exception as e:  # pragma: no cover
    print("This script requires the 'beautifulsoup4' package.", file=sys.stderr)
    raise


URL_RE = re.compile(r"https?://[^\s<>]+")


def read_urls_from_markdown(path: str) -> List[str]:
    urls: List[str] = []
    seen = set()
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            # Accept bullets like '- https://...'
            if line.startswith("-"):
                m = URL_RE.search(line)
                if m:
                    url = m.group(0)
                else:
                    continue
            else:
                m = URL_RE.search(line)
                if m:
                    url = m.group(0)
                else:
                    continue
            if url not in seen:
                seen.add(url)
                urls.append(url)
    return urls


def build_http_session() -> requests.Session:
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=0.3,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({
        "User-Agent": "pyeverything-docs-collector/1.0 (+https://github.com/)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    })
    return session


def page_title_from_url(url: str) -> str:
    # Use the last path segment as a fallback title
    seg = url.rstrip("/").rsplit("/", 1)[-1]
    seg = seg.replace("_", " ")
    return seg


def clean_text(s: str) -> str:
    s = s.replace("\r", "\n")
    # Normalize multiple blank lines
    s = re.sub(r"\n\s*\n\s*\n+", "\n\n", s)
    return s.strip()


def html_to_markdown(node: Tag) -> str:
    lines: List[str] = []

    def render(el: Tag, level: int = 0) -> None:
        if isinstance(el, NavigableString):
            text = str(el)
            if text.strip():
                lines.append(text)
            return

        name = getattr(el, "name", "")
        if name in ("script", "style", "noscript", "header", "footer", "nav", "aside"):
            return

        # Headings
        if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(name[1])
            prefix = "#" * min(6, level + 1)  # offset headings under page H2+ later
            text = el.get_text(" ", strip=True)
            if text:
                lines.append(f"{prefix} {text}")
            return

        if name == "p":
            text = el.get_text(" ", strip=True)
            if text:
                lines.append(text)
            lines.append("")
            return

        if name in ("ul", "ol"):
            for li in el.find_all("li", recursive=False):
                li_text = li.get_text(" ", strip=True)
                if li_text:
                    lines.append(f"- {li_text}")
            lines.append("")
            return

        if name == "pre":
            code = el.get_text("\n", strip=False)
            lines.append("```")
            lines.append(code.rstrip("\n"))
            lines.append("```")
            lines.append("")
            return

        # Fallback: render children
        for child in el.children:
            if isinstance(child, (NavigableString, Tag)):
                render(child, level)

    render(node)
    text = "\n".join(lines)
    # Collapse excessive blank lines
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    return text.strip()


def pick_main_content(soup: BeautifulSoup) -> Tag:
    # Prefer common content containers
    candidates = [
        soup.select_one("#content"),
        soup.select_one("#wikicontent"),
        soup.select_one("article"),
        soup.select_one(".content"),
        soup.select_one("#main"),
        soup.select_one("#bodyContent"),
    ]
    for c in candidates:
        if c:
            return c

    # Otherwise, choose the element containing the first h1
    h1 = soup.find("h1")
    if h1 and h1.parent:
        return h1.parent

    # Fallback to body
    return soup.body or soup


def sanitize_dom(root: Tag) -> None:
    # Remove common non-content sections
    for sel in [
        "script", "style", "noscript", "header", "footer", "nav", "aside",
        ".wikinavindent1", ".wikinavindent2", ".wikinavindent3", ".sidebar", ".breadcrumbs",
        "#header", "#footer", "#sidebar",
    ]:
        for el in root.select(sel):
            el.decompose()


@dataclass
class PageResult:
    url: str
    title: str
    markdown: str
    error: Optional[str] = None


def fetch_and_extract(session: requests.Session, url: str, timeout: float = 15.0) -> PageResult:
    title = page_title_from_url(url)
    try:
        r = session.get(url, timeout=timeout)
        r.raise_for_status()
    except Exception as e:
        return PageResult(url=url, title=title, markdown="", error=str(e))

    soup = BeautifulSoup(r.text, "lxml") if "lxml" in sys.modules else BeautifulSoup(r.text, "html.parser")
    content = pick_main_content(soup)
    sanitize_dom(content)
    md = html_to_markdown(content)
    md = clean_text(md)
    return PageResult(url=url, title=title, markdown=md)


def write_reference(path: str, pages: List[PageResult]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Everything SDK Reference\n\n")
        f.write("This document aggregates function reference pages from the Everything wiki.\n\n")
        for p in pages:
            section_title = p.title.strip() or page_title_from_url(p.url)
            f.write(f"## {section_title}\n\n")
            f.write(f"Source: {p.url}\n\n")
            if p.error:
                f.write(f"Error fetching page: {p.error}\n\n")
                continue
            f.write(p.markdown)
            f.write("\n\n")


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Build Everything SDK reference from a list of URLs")
    ap.add_argument("--input", required=True, help="Path to markdown file containing URLs (one per line or bullet)")
    ap.add_argument("--output", required=True, help="Path to write consolidated reference markdown")
    ap.add_argument("--workers", type=int, default=8, help="Concurrent fetch workers")
    return ap.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    urls = read_urls_from_markdown(args.input)
    if not urls:
        print(f"No absolute URLs found in {args.input}", file=sys.stderr)
        return 2

    session = build_http_session()
    pages: List[PageResult] = [None] * len(urls)  # type: ignore
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        future_to_idx = {
            ex.submit(fetch_and_extract, session, url): i for i, url in enumerate(urls)
        }
        for fut in concurrent.futures.as_completed(future_to_idx):
            i = future_to_idx[fut]
            try:
                pages[i] = fut.result()
            except Exception as e:  # pragma: no cover
                pages[i] = PageResult(url=urls[i], title=page_title_from_url(urls[i]), markdown="", error=str(e))

    write_reference(args.output, pages)  # preserves order from input
    print(f"Wrote {args.output} with {len(pages)} sections")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

