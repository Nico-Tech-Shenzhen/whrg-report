#!/usr/bin/env python3
"""Validate headline report numbers against the reviewed event ledger."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "research" / "evidence" / "event-report-2026.json"


def require(condition: bool, message: str, issues: list[str]) -> None:
    if not condition:
        issues.append(message)


def main() -> int:
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    competitions = data["competitions"]
    by_id = {item["Competition ID"]: item for item in competitions}
    medals = [item for item in data["medal_ledger"]
              if item.get("Official Team Name") not in (None, "", "[Unknown]")]
    medal_counts = Counter(item["Medal"] for item in medals)
    issues: list[str] = []

    require(len(competitions) == 51, "competition count must be 51", issues)
    require(sum(1 for item in competitions
                if int(item["Competition ID"].split("-")[1]) >= 31) == 21,
            "real-world task count must be 21", issues)
    require(len(data["medal_ledger"]) == 159, "medal-slot count must be 159", issues)
    require(len(medals) == 136, "resolved medal-slot count must be 136", issues)
    require(medal_counts == Counter({"Gold": 47, "Silver": 44, "Bronze": 45}),
            f"resolved medal counts changed: {dict(medal_counts)}", issues)
    require(str(by_id["C-002"]["Winning result / score"]).startswith("8.64"),
            "100-metre winning mark must be 8.64 seconds", issues)
    require("305.000" in str(by_id["C-039"]["Winning result / score"])
            and "26:12" in str(by_id["C-039"]["Winning result / score"]),
            "domestic-service winning result changed", issues)

    required_public = {
        ROOT / "docs" / "index.md": ("第2回", "8月22日", "26日", "16か国", "666", "2,056", "51種目", "30", "21", "1,301", "12の応用場面"),
        ROOT / "docs" / "ch01.md": ("8.64", "10対1", "305", "26分12秒"),
        ROOT / "docs" / "ch02.md": ("全51種目", "完全自律", "遠隔0.5"),
        ROOT / "docs" / "ch03.md": ("21種目", "12の応用場面", "3車種"),
        ROOT / "docs" / "ch05.md": ("2,500時間超", "12の応用場面", "44種類の作業", "100種類超の技能", "1万件超の詳細タスク"),
        ROOT / "docs" / "ch04.md": ("159", "136", "47", "44", "45", "23"),
        ROOT / "docs" / "ch06.md": ("2026年10月13日",),
        ROOT / "docs" / "appendix.md": ("51", "159", "23"),
    }
    for path, tokens in required_public.items():
        if not path.is_file():
            issues.append(f"missing report file: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        for token in tokens:
            require(token in text, f"{path.relative_to(ROOT)} must contain {token!r}", issues)

    chapter_2 = (ROOT / "docs" / "ch02.md").read_text(encoding="utf-8")
    chapter_2_rows = []
    for line in chapter_2.splitlines():
        if line.startswith("| "):
            first_cell = line.split("|", 2)[1].strip()
            if first_cell.isdigit():
                chapter_2_rows.append(int(first_cell))
    require(chapter_2_rows == list(range(1, 52)),
            "Chapter 2 reader inventory must contain event rows 1 through 51 exactly once", issues)

    if issues:
        print("FAIL: number validation")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("OK: headline numbers match the reviewed event ledger.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
