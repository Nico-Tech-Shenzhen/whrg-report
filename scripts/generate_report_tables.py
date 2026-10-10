#!/usr/bin/env python3
"""Generate reader-facing summary tables from the canonical research corpus."""

from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
RECORDS = ROOT / "research" / "evidence" / "records.json"
OUTPUT = ROOT / "docs" / "data-tables.md"


def relation_targets(record: dict, relation: str, entity_type: str | None = None) -> list[str]:
    targets = []
    for item in record.get("relationships", []):
        target = item.get("target", {})
        if item.get("relation") == relation and (entity_type is None or target.get("entity_type") == entity_type):
            targets.append(target.get("id", ""))
    return [target for target in targets if target]


def main() -> None:
    records = json.loads(RECORDS.read_text(encoding="utf-8"))
    by_type: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        by_type[record["entity_type"]].append(record)

    competitions = {record["id"]: record for record in by_type["Competition"]}
    entries = by_type["Competition Entry"]
    teams = {record["id"]: record for record in by_type["Team"]}

    entry_counts = Counter(entry.get("entry", {}).get("competition_id") for entry in entries)
    verified_counts = Counter()
    participation_by_competition: dict[str, Counter] = defaultdict(Counter)
    participation_total = Counter()
    team_competitions: dict[str, set[str]] = defaultdict(set)
    for entry in entries:
        data = entry.get("entry", {})
        competition_id = data.get("competition_id")
        verification = entry.get("verification", {}).get("canonical_status", "Unknown")
        verified_counts[(competition_id, verification)] += 1
        participation = data.get("participation_status") or "Unknown"
        participation_by_competition[competition_id][participation] += 1
        participation_total[participation] += 1
        team_id = data.get("team_id")
        if team_id and competition_id:
            team_competitions[team_id].add(competition_id)

    entity_counts = Counter(record["entity_type"] for record in records)
    linked_entries = sum(bool(entry.get("entry", {}).get("team_id")) for entry in entries)
    organization_teams = sum(
        any(rel.get("target", {}).get("entity_type") == "Organization" for rel in team.get("relationships", []))
        for team in teams.values()
    )
    joint_teams = sum(
        any(rel.get("relation") == "joint_team_member" for rel in team.get("relationships", []))
        for team in teams.values()
    )
    robot_teams = sum(
        any(rel.get("relation") == "used_robot_platform" for rel in team.get("relationships", []))
        for team in teams.values()
    )
    robot_entries = sum(bool(entry.get("entry", {}).get("robot_id")) for entry in entries)

    lines = [
        "# 再構成データ集計表",
        "",
        "このページは本調査の canonical data から生成した集計である。公式発表の総参加チーム数ではなく、本調査が公開資料から再構成できた Competition Entry を数える。生成日時に依存する外部検索は行わない。公式規程は51競技の構成を示し、公式の成績公告群が Entry 再構成の主要な根拠となる。[[1]](#ref-1)[[2]](#ref-2)",
        "",
        "## 正規化済みエンティティ数",
        "",
        "| 種別 | 件数 |",
        "| --- | ---: |",
    ]
    display_order = ["Competition", "Competition Entry", "Team", "Organization", "Robot Platform", "Evidence", "Rule Version"]
    for name in display_order:
        lines.append(f"| {name} | {entity_counts[name]} |")
    lines.extend([
        "",
        "| リンク指標 | 件数 |",
        "| --- | ---: |",
        f"| Team にリンクした Competition Entry | {linked_entries} / {len(entries)} |",
        f"| Organization 関係を持つ Team | {organization_teams} / {len(teams)} |",
        f"| joint_team_member 関係を持つ Team | {joint_teams} |",
        f"| Robot Platform 使用関係を持つ Team | {robot_teams} / {len(teams)} |",
        f"| Robot Platform ID を持つ Competition Entry | {robot_entries} / {len(entries)} |",
        "",
        "## 参加状態",
        "",
        "参加状態は本調査の正規化値であり、Finished は完走・完了、DNF は開始後未完了、DNS は出場記録なし、Disqualified は失格、Started は開始確認済みだが完了未確認、Scheduled は予定・組合せのみ確認、Unknown は判定材料不足を表す。",
        "",
        "| 状態 | Entry数 |",
        "| --- | ---: |",
    ])
    status_order = ["Finished", "Started", "Scheduled", "DNS", "DNF", "Disqualified", "Unknown"]
    for status in status_order:
        if participation_total[status]:
            lines.append(f"| {status} | {participation_total[status]} |")

    lines.extend([
        "",
        "## 競技別 Competition Entry 数",
        "",
        "| 競技 | 種別 | Entry | Verified | Research Lead | Finished | その他 |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ])
    for competition_id in sorted(competitions, key=lambda value: int(value.split("-")[1])):
        competition = competitions[competition_id]
        category = competition.get("competition", {}).get("category") or "Unknown"
        total = entry_counts[competition_id]
        finished = participation_by_competition[competition_id]["Finished"]
        lines.append(
            f"| {competition['label']} | {category} | {total} | "
            f"{verified_counts[(competition_id, 'Verified')]} | "
            f"{verified_counts[(competition_id, 'Research Lead')]} | {finished} | {total - finished} |"
        )

    recurring = sorted(
        ((team_id, competition_ids) for team_id, competition_ids in team_competitions.items() if len(competition_ids) > 1),
        key=lambda item: (-len(item[1]), teams[item[0]]["label"], item[0]),
    )
    lines.extend([
        "",
        "## 複数競技に現れる Team",
        "",
        f"正規化済み Team のうち、複数競技に対応するものは {len(recurring)} 件である。上位20件のみを示す。名称一致だけでなく canonical Team ID を基準に集計した。",
        "",
        "| Team | 競技数 |",
        "| --- | ---: |",
    ])
    for team_id, competition_ids in recurring[:20]:
        lines.append(f"| {teams[team_id]['label']} | {len(competition_ids)} |")

    lines.extend([
        "",
        "## 参考文献",
        "",
        '<a id="ref-1"></a>1. [世界人形机器人运动会组委会「第二届世界人形机器人运动会竞赛规程总则」](https://www.whrgoc.com/documents/2072500150398033920)（2026年7月2日）。',
        "",
        '<a id="ref-2"></a>2. [世界人形机器人运动会组委会「第二届世界人形机器人运动会田径400米（大型组）决赛成绩公告」](https://www.whrgoc.com/resources//uploads/20260823/1787498892357039182.pdf)（2026年8月23日、公式成績公告の一例）。',
        "",
    ])
    content = "\n".join(lines)
    if "--check" in sys.argv[1:]:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != content:
            print(f"FAIL: generated report tables are stale: {OUTPUT}")
            raise SystemExit(1)
        print(f"OK: generated report tables are current: {OUTPUT}")
        return
    OUTPUT.write_text(content, encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
