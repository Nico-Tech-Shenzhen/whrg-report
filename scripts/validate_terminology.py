#!/usr/bin/env python3
"""Validate reader-facing Markdown against forbidden forms in dic.md."""

from __future__ import annotations

import sys
from pathlib import Path

from text_validation import report_files, visible_lines


def rules(dictionary: Path = Path("dic.md")) -> list[tuple[str, str]]:
    parsed: list[tuple[str, str]] = []
    for line in dictionary.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or "---" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 5 or cells[0] == "Source form":
            continue
        canonical, forbidden = cells[2], cells[3]
        for term in forbidden.split(";"):
            term = term.strip()
            if term and term != "—":
                parsed.append((term, canonical))
    return parsed


def find_issues(paths: list[Path]) -> list[tuple[Path, int, str, str]]:
    issues = []
    term_rules = rules()
    for path in paths:
        for number, line in visible_lines(path):
            for forbidden, canonical in term_rules:
                if forbidden in line:
                    issues.append((path, number, forbidden, canonical))
    return issues


def main() -> int:
    term_rules = rules()
    issues = find_issues(report_files())
    if issues:
        print(f"FAIL: {len(issues)} forbidden terminology occurrence(s)")
        for path, number, forbidden, canonical in issues:
            print(f"{path}:{number}: {forbidden!r} -> {canonical}")
        return 1
    print(f"OK: terminology passed ({len(term_rules)} forbidden forms checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
