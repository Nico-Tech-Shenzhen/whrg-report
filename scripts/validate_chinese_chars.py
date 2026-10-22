#!/usr/bin/env python3
"""Detect unmarked Simplified Chinese in Japanese reader-facing prose."""

from __future__ import annotations

import sys

from text_validation import report_files, visible_lines

SIMPLIFIED = set(
    "赛场项预决运动车辆门务业图发开现实时队际标准统计组织"
    "录线过达长为寻应仓储饮书园电关联进处评获奖"
)
PHRASES = ("机器人运动会", "竞技赛", "场景赛", "全自主", "遥操作", "数据集")


def find_issues(paths=None):
    issues = []
    paths = report_files() if paths is None else paths
    for path in paths:
        for number, line in visible_lines(path):
            phrase_hits = [phrase for phrase in PHRASES if phrase in line]
            chars = "".join(sorted({char for char in line if char in SIMPLIFIED}))
            if phrase_hits or chars:
                issues.append((path, number, ", ".join(phrase_hits) or chars))
    return issues


def main() -> int:
    issues = find_issues()
    if issues:
        print(f"FAIL: {len(issues)} unmarked Simplified-Chinese occurrence(s)")
        for path, number, token in issues:
            print(f"{path}:{number}: {token}")
        return 1
    print("OK: no unmarked Simplified Chinese found in reader-facing prose.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
