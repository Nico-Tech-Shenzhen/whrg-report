#!/usr/bin/env python3
"""Reject internal research vocabulary from Japanese reader-facing prose."""

from __future__ import annotations

import re
import sys

from text_validation import report_files, visible_lines

INTERNAL_TERMS = (
    "Competition Entry", "Robot Platform", "Rule Version", "Organization",
    "Competition", "Evidence", "Dataset", "License", "Team",
)


def find_issues(paths=None):
    issues = []
    paths = report_files() if paths is None else paths
    patterns = [(term, re.compile(rf"(?<![A-Za-z]){re.escape(term)}(?![A-Za-z])"))
                for term in INTERNAL_TERMS]
    for path in paths:
        for number, line in visible_lines(path):
            for term, pattern in patterns:
                if pattern.search(line):
                    issues.append((path, number, term))
    return issues


def main() -> int:
    issues = find_issues()
    if issues:
        print(f"FAIL: {len(issues)} internal-English occurrence(s)")
        for path, number, term in issues:
            print(f"{path}:{number}: {term}")
        return 1
    print("OK: Japanese prose contains no internal English schema labels.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
