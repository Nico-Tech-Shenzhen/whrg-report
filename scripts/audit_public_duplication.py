#!/usr/bin/env python3
"""Report suspicious repeated prose across public Markdown pages.

This is an editorial signal, not an automatic deletion rule. Reference lists,
tables, headings, navigation-like short text, and Markdown links are excluded.
"""

from __future__ import annotations

import argparse
from difflib import SequenceMatcher
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MIN_CHARS = 48


def public_files() -> list[Path]:
    files = [DOCS / "index.md"]
    files.extend(sorted(DOCS.glob("ch[0-9][0-9].md")))
    files.append(DOCS / "appendix.md")
    return [path for path in files if path.is_file()]


def normalize(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\[\[[0-9]+\]\]\(#ref-[0-9]+\)", "", text)
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[`*_～〜・、。！？：；（）()\[\]{}『』「」\s]", "", text)
    return text.lower()


def units(path: Path) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    paragraph: list[str] = []
    start = 0
    in_references = False

    def flush() -> None:
        nonlocal paragraph, start
        if not paragraph:
            return
        raw = " ".join(paragraph).strip()
        value = normalize(raw)
        if len(value) >= MIN_CHARS:
            result.append({"file": path.name, "line": start, "text": raw, "normalized": value})
        paragraph = []

    for number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if line.startswith("## "):
            flush()
            in_references = line[3:] == "参考文献"
            continue
        if in_references:
            continue
        if not line or line.startswith(("#", "|", "- ")) or re.match(r"^\d+\. ", line):
            flush()
            continue
        if not paragraph:
            start = number
        paragraph.append(line)
    flush()
    return result


def ngrams(value: str, size: int = 5) -> set[str]:
    return {value[index:index + size] for index in range(max(0, len(value) - size + 1))}


def audit() -> dict[str, object]:
    items = [item for path in public_files() for item in units(path)]
    exact: list[dict[str, object]] = []
    similar: list[dict[str, object]] = []
    for index, left in enumerate(items):
        for right in items[index + 1:]:
            if left["file"] == right["file"]:
                continue
            a = str(left["normalized"])
            b = str(right["normalized"])
            if a == b:
                exact.append({"left": f'{left["file"]}:{left["line"]}', "right": f'{right["file"]}:{right["line"]}', "characters": len(a)})
                continue
            shorter = min(len(a), len(b))
            longer = max(len(a), len(b))
            if shorter / longer < 0.62:
                continue
            ag = ngrams(a)
            bg = ngrams(b)
            overlap = len(ag & bg) / max(1, min(len(ag), len(bg)))
            sequence = SequenceMatcher(None, a, b, autojunk=False).ratio()
            if overlap >= 0.72 and sequence >= 0.68:
                similar.append({
                    "left": f'{left["file"]}:{left["line"]}',
                    "right": f'{right["file"]}:{right["line"]}',
                    "ngram_overlap": round(overlap, 3),
                    "sequence_ratio": round(sequence, 3),
                })
    return {"files": len(public_files()), "paragraphs": len(items), "exact": exact, "high_overlap": similar}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--fail-on-suspects", action="store_true")
    args = parser.parse_args()
    result = audit()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f'Files: {result["files"]}; paragraphs: {result["paragraphs"]}')
        print(f'Exact cross-page duplicates: {len(result["exact"])}')
        print(f'High-overlap cross-page pairs: {len(result["high_overlap"])}')
        for group in ("exact", "high_overlap"):
            for item in result[group]:
                print(f'{group}: {item["left"]} <-> {item["right"]}')
    return 1 if args.fail_on_suspects and (result["exact"] or result["high_overlap"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
