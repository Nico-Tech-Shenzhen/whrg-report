#!/usr/bin/env python3
"""Shared helpers for reader-facing Markdown validation."""

from __future__ import annotations

import re
from pathlib import Path

INLINE_CODE = re.compile(r"`[^`]*`")
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\([^)]*\)")
URL = re.compile(r"https?://\S+")
HTML_OFFICIAL_NAME = re.compile(r'<span\s+lang=["\x27](?:zh|en)["\x27][^>]*>.*?</span>', re.I)
JAPANESE_QUOTE = re.compile(r"[「『][^」』]*[」』]")
OFFICIAL_ANNOTATION = re.compile(r"（[^（）]*(?:公司|大学|研究院|机器人|数据集|World|Team)[^（）]*）")


def visible_lines(path: Path):
    """Yield prose lines with allowed source/identifier zones masked."""
    fenced = False
    in_references = False
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if raw.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if re.match(r"^##+\s+(参考文献|References)\s*$", raw):
            in_references = True
        if in_references:
            continue
        line = raw
        for pattern in (HTML_OFFICIAL_NAME, MARKDOWN_LINK, URL, INLINE_CODE,
                        JAPANESE_QUOTE, OFFICIAL_ANNOTATION):
            line = pattern.sub("", line)
        yield number, line


def report_files(root: Path = Path("docs")) -> list[Path]:
    preferred = [root / "index.md"]
    preferred.extend(root / f"ch{number:02d}.md" for number in range(1, 10))
    preferred.append(root / "appendix.md")
    return [path for path in preferred if path.is_file()]
