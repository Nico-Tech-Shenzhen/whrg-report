#!/usr/bin/env python3
"""Flag rhetorical negation and report-process prose in public Markdown."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from text_validation import report_files, visible_lines


PHRASES = (
    "だけではない",
    "だけでなく",
    "単なる",
    "単に",
    "ではなく",
    "を意味しない",
    "本報告が問う",
    "本章では",
    "本章は",
    "重要なのは",
    "ここでは",
    "次章では",
)

# Legitimate negative facts may be retained after line-specific editorial review.
# Entries are (repository-relative path, line number, phrase).
REVIEWED_OCCURRENCES: set[tuple[str, int, str]] = set()


@dataclass(frozen=True)
class Occurrence:
    path: Path
    line: int
    phrase: str
    text: str
    reviewed: bool


def find_occurrences(
    paths: list[Path],
    reviewed: set[tuple[str, int, str]] | None = None,
) -> list[Occurrence]:
    """Return visible phrase occurrences, including explicitly reviewed ones."""
    allowed = REVIEWED_OCCURRENCES if reviewed is None else reviewed
    occurrences: list[Occurrence] = []
    for path in paths:
        display = path.as_posix()
        for line_number, line in visible_lines(path):
            for phrase in PHRASES:
                if phrase not in line:
                    continue
                key = (display, line_number, phrase)
                occurrences.append(
                    Occurrence(path, line_number, phrase, line.strip(), key in allowed)
                )
    return occurrences


def main() -> int:
    occurrences = find_occurrences(report_files())
    for item in occurrences:
        state = "REVIEWED" if item.reviewed else "UNRESOLVED"
        print(f"{state}: {item.path}:{item.line}: {item.phrase}: {item.text}")
    unresolved = [item for item in occurrences if not item.reviewed]
    if unresolved:
        print(f"FAIL: {len(unresolved)} unresolved positive-prose occurrence(s).")
        return 1
    print(
        "OK: positive-prose lint passed "
        f"({len(occurrences)} reviewed occurrence(s), 0 unresolved)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
