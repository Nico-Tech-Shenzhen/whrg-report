#!/usr/bin/env python3
"""Validate reader-facing Markdown against forbidden terms in dic.md."""

from __future__ import annotations
import re
import sys
from pathlib import Path

LINK = re.compile(r"\[[^]]*\]\([^)]*\)")
URL = re.compile(r"https?://\S+")
INLINE_CODE = re.compile(r"`[^`]*`")


def rules() -> list[tuple[str, str]]:
    parsed = []
    for line in Path("dic.md").read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or "---" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if "Canonical" in cells:
            continue
        if len(cells) == 5:
            canonical, forbidden = cells[2], cells[3]
        elif len(cells) == 4:
            canonical, forbidden = cells[1], cells[2]
        else:
            continue
        for term in forbidden.split(";"):
            if term.strip() and term.strip() != "\u2014":
                parsed.append((term.strip(), canonical))
    return parsed


def visible_lines(path: Path):
    fenced = in_references = False
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if raw.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if raw.startswith(("## References", "## \u53c2\u8003\u6587\u732e")):
            in_references = True
        if not in_references:
            yield number, INLINE_CODE.sub("", URL.sub("", LINK.sub(lambda m: m.group(0).split("](", 1)[0].lstrip("["), raw)))


def main() -> int:
    issues = []
    term_rules = rules()
    for path in sorted(Path("docs").rglob("*.md")):
        for number, line in visible_lines(path):
            for forbidden, canonical in term_rules:
                if forbidden in line:
                    issues.append((path, number, forbidden, canonical))
    if issues:
        print(f"FAIL: {len(issues)} forbidden terminology occurrence(s)")
        for path, number, forbidden, canonical in issues:
            print(f"{path}:{number}: {forbidden!r} -> {canonical}")
        return 1
    print(f"OK: terminology passed ({len(term_rules)} forbidden forms checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
