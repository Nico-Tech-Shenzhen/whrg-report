#!/usr/bin/env python3
"""Generate reviewed WHRG 2026 event tables from immutable Kimi snapshots."""

from __future__ import annotations

from collections import OrderedDict
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

import openpyxl


ROOT = Path(__file__).resolve().parents[1]
EVENT_SHA = "320ab83cd4a8150ecbdc67cc3262f9289c85f2ef7ac0443cb43ee6a9e198b8d3"
DATASET_SHA = "7458ce35ae1dbb3e8708aa04517f789d792924ddcd393445eb34b045fd4e338c"
EVENT_BOOK = ROOT / "research" / "imported" / "kimi" / EVENT_SHA / "whrg-2026-event-results-report-research.xlsx"
DATASET_BOOK = ROOT / "research" / "imported" / "kimi" / DATASET_SHA / "whrg-2026-dataset-release-audit.xlsx"
RECORDS = ROOT / "research" / "evidence" / "records.json"
DATA_OUTPUT = ROOT / "research" / "evidence" / "event-report-2026.json"


TASK_JA = {
    "C-001": "静止状態から100mを走り、完走時間を競う（小型級）。",
    "C-002": "静止状態から100mを走り、完走時間を競う（大型級）。",
    "C-003": "400mトラックを走り、完走時間を競う（小型級）。",
    "C-004": "400mトラックを走り、完走時間を競う（大型級）。",
    "C-005": "1500mを走り切る持久走。完走時間で順位を決める。",
    "C-006": "複数ロボットで4区間をつなぐ400mリレー。完走時間を競う。",
    "C-007": "100mの障害コースを通過し、完走と所要時間を競う。",
    "C-008": "400mの障害コースを通過し、所要時間を競う。",
    "C-009": "助走なしで前方へ跳び、着地点までの距離を測る。",
    "C-010": "助走から踏み切って跳び、跳躍距離を測る。",
    "C-011": "その場から上方へ跳び、到達した高さを測る。",
    "C-012": "大型ロボット5台対5台で自律サッカーを行い、得点で勝敗を決める。",
    "C-013": "中型ロボット5台対5台で自律サッカーを行う。",
    "C-014": "U19チームが中型ロボット3台対3台で自律サッカーを行う。",
    "C-015": "床上で規定時間の体操演技を行い、審査員が採点する。",
    "C-016": "40kg未満の機体がバーベルを持ち上げ、2秒保持できた最大重量を競う。",
    "C-017": "40kg超80kg以下の機体がバーベルを持ち上げ、成功した最大重量を競う。",
    "C-018": "ロボットがストリートダンスを自律演技し、9人の審査員が採点する。",
    "C-019": "国際標準舞の演技を行い、表現と動作を採点する。",
    "C-020": "チアダンスの演技を行い、審査得点を競う。",
    "C-021": "白鶴亮翅などの指定動作を含む太極拳を演じ、完成度を採点する。",
    "C-022": "任意の武術套路を演じ、技術と完成度を採点する。",
    "C-023": "軽量級ロボット同士が綱を引き、複数ラウンドの勝敗を競う。",
    "C-024": "重量級ロボット同士が綱を引き、複数ラウンドの勝敗を競う。",
    "C-025": "車輪型ロボットが矢を壺へ投げ、命中精度を競う。",
    "C-026": "二足ロボットが矢を壺へ投げ、命中精度を競う。",
    "C-027": "卓球を行い、グループ戦と決勝トーナメントの勝敗で順位を決める。",
    "C-028": "40・58・80kg級で自律格闘を行い、判定・KO・レフェリーストップで勝敗を決める。",
    "C-029": "開幕時にテニスのエキシビションが行われたが、正式競技結果は未確認。",
    "C-030": "公式規程と競技一覧の不一致により、第30競技の同定が未完了。",
    "C-031": "五つの異なる作業を連続実行し、長いタスク列の総合得点を競う。",
    "C-032": "20分で注文品を選び、棚を巡回し、補充と誤配置商品の修正を行う。",
    "C-033": "食品を取り、電子レンジを操作し、飲料とともに客へ届ける。",
    "C-034": "製品を梱包し、ラベルを貼り、倉庫へ入庫する一連の工程を行う。",
    "C-035": "部品を運搬・識別・仕分けし、エンジン部品へ精密に挿入する。",
    "C-036": "消防現場を模した処置を行い、完了タスクと時間を採点する。",
    "C-037": "突発事態への緊急対応手順を実行し、達成した作業を採点する。",
    "C-038": "オフィス内の印刷物・物品の配達や整理など、複数のサービスを行う。",
    "C-039": "30分で片付け、宅配受取、洗濯、衣類たたみ・物干しを連続実行する。",
    "C-040": "ホテル客室の整理と宿泊客向けサービスを行う。",
    "C-041": "図書を識別・分類し、指定位置へ配架・整理する。",
    "C-042": "園区内を巡回し、点検・管理作業を行う。",
    "C-043": "電気自動車の充電コネクタを扱い、充電サービス工程を行う。",
    "C-044": "デックスハンドで電動工具の部品を組み立てる。",
    "C-045": "デックスハンドで微量の粉末を扱い、指定量を計量する。",
    "C-046": "小さなブロックを把持し、指定された構造を組み立てる。",
    "C-047": "釘と工具を扱い、対象物へ打ち込んで固定する。",
    "C-048": "瓶や容器を把持し、栓・蓋を開ける。",
    "C-049": "箱と包装材を扱い、中身を傷めず開梱する。",
    "C-050": "ピンセットを操作し、小さな豆粒をつまんで移す。",
    "C-051": "細いケーブルとコネクタを把持し、正しく接続する。",
}

DEXTEROUS_RESULT_IDS = {
    "C-044": "EV-0098",
    "C-045": "EV-0091",
    "C-046": "EV-0090",
    "C-047": "EV-0106",
    "C-048": "EV-0109",
    "C-049": "EV-0107",
    "C-050": "EV-0092",
    "C-051": "EV-0108",
}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def rows(book: Path, sheet: str) -> list[dict]:
    workbook = openpyxl.load_workbook(book, read_only=True, data_only=True, keep_links=False)
    worksheet = workbook[sheet]
    iterator = worksheet.iter_rows(values_only=True)
    headers = [str(value) if value is not None else "" for value in next(iterator)]
    result = [dict(zip(headers, row)) for row in iterator if any(value is not None for value in row)]
    workbook.close()
    return result


def evidence_map(book: Path) -> dict[str, dict]:
    return {str(item["Evidence ID"]): item for item in rows(book, "Evidence Map")}


def canonical_evidence() -> dict[str, dict]:
    records = json.loads(RECORDS.read_text(encoding="utf-8"))
    return {item["id"]: item for item in records if item.get("entity_type") == "Evidence"}


def condition_ja(item: dict) -> str:
    number = int(str(item["Competition ID"]).split("-")[1])
    if number in (7, 8):
        return "自律重視。規則上の限定補助あり"
    if number in (29, 30):
        return "未確認"
    if number >= 31:
        return "自律1.0、遠隔操作0.5"
    return "全自律。遠隔操作なし"


def score_ja(item: dict) -> str:
    text = str(item.get("Scoring basis") or "")
    if "Task score" in text or text == "同上":
        return "作業点×自律係数−減点"
    if "Time" in text:
        return "完走時間"
    if "Distance" in text:
        return "跳躍距離"
    if "Height" in text:
        return "到達高さ"
    if "Match score" in text:
        return "試合得点・勝敗"
    if "Judged" in text:
        return "審査員得点"
    if "Max successful" in text:
        return "成功した最大重量"
    if "Best-of" in text:
        return "ラウンド勝敗"
    if "Accuracy" in text:
        return "命中精度"
    if "WP/KO/RSC" in text:
        return "判定・KO・RSC"
    return "未確認"


def resolve_source(item: dict, event_evidence: dict[str, dict], canonical: dict[str, dict]) -> tuple[str, str] | None:
    direct_id = DEXTEROUS_RESULT_IDS.get(str(item.get("Competition ID")))
    if direct_id:
        record = canonical[direct_id]
        return record["label"], record["source"]["url"]
    keys = [key.strip() for key in str(item.get("Official result Evidence") or "").split(",")]
    for key in keys:
        evidence = event_evidence.get(key)
        if not evidence:
            continue
        locator = str(evidence.get("URL / locator") or "")
        if locator.startswith("http"):
            return str(evidence["Title"]), locator
        tokens = re.findall(r"(?:ATT|EV)-\d+", locator)
        for token in tokens:
            record = canonical.get(token)
            if record and str(record.get("source", {}).get("url", "")).startswith("http"):
                return record["label"], record["source"]["url"]
        filenames = re.findall(r"\d{19}\.pdf", locator)
        for record in canonical.values():
            url = str(record.get("source", {}).get("url", ""))
            if filenames and any(filename in url for filename in filenames):
                return record["label"], url
    return None


def reviewed_data() -> dict:
    if digest(EVENT_BOOK) != EVENT_SHA or digest(DATASET_BOOK) != DATASET_SHA:
        raise ValueError("Immutable workbook hash mismatch")
    competitions = rows(EVENT_BOOK, "B-Competition Results 51")
    medal_ledger = rows(EVENT_BOOK, "C4-Medal Ledger")
    team_medals = rows(EVENT_BOOK, "C4-A by Team")
    event_sources = evidence_map(EVENT_BOOK)
    canonical = canonical_evidence()
    resolved_sources = {}
    for item in competitions:
        source = resolve_source(item, event_sources, canonical)
        if source:
            resolved_sources[item["Competition ID"]] = {"title": source[0], "url": source[1]}
    return {
        "reviewed_at": "2026-10-10",
        "source_snapshots": {"event_results": EVENT_SHA, "dataset_audit": DATASET_SHA},
        "review_status": "reviewed_for_public_report_not_wholesale_canonical_promotion",
        "competitions": competitions,
        "resolved_result_sources": resolved_sources,
        "medal_ledger": medal_ledger,
        "team_medals": team_medals,
        "dataset_claims": rows(DATASET_BOOK, "F-Dataset Claims"),
        "dataset_openness": rows(DATASET_BOOK, "I-Openness Status"),
        "dataset_organizations": rows(DATASET_BOOK, "G-Organizations"),
        "dataset_comparison": rows(DATASET_BOOK, "J-vs Existing Datasets"),
        "dataset_sources": list(evidence_map(DATASET_BOOK).values()),
        "post_event": rows(EVENT_BOOK, "K-Post-Event Outcomes"),
    }


def competition_page(data: dict) -> str:
    refs: OrderedDict[str, tuple[int, str]] = OrderedDict()

    def cite(cid: str) -> str:
        source = data["resolved_result_sources"].get(cid)
        if not source:
            return "未確認"
        if source["url"] not in refs:
            refs[source["url"]] = (len(refs) + 1, source["title"])
        return f'[[{refs[source["url"]][0]}]](#ref-{refs[source["url"]][0]})'

    lines = [
        "# 51競技と結果",
        "",
        "WHRG 2026の公式競技体系は、走る・跳ぶ・球技・格闘などの競技赛30種と、家庭・産業・サービス現場を模した场景赛21種から成る。ここでは内部IDではなく、ロボットが実際に何を求められたかを中心に示す。公式結果を確認できない欄は推測で埋めていない。[[1]](#ref-1)",
        "",
        "场景赛では原則として自律実行を1.0、遠隔操作を0.5の係数で評価した。同じ順位表でも、作業点と自律係数の双方を読まなければ自律性能の比較にはならない。[[2]](#ref-2)",
        "",
    ]
    # Reserve the first two references for the rules and autonomy explanation.
    refs["https://www.whrgoc.com/documents/2072500150398033920"] = (1, "第二届世界人形机器人运动会竞赛规程总则")
    refs["https://dt.sheitc.sh.gov.cn/cms/gntsqqsjyw/2886.jhtml"] = (2, "上海市经济和信息化委员会：数智要闻")
    categories = [
        ("陸上・走競技", {"田径"}),
        ("サッカー・球技", {"球类"}),
        ("体操・ダンス", {"体操舞蹈"}),
        ("格闘・武術", {"武术", "对抗"}),
        ("力・技巧競技", {"力量", "技巧"}),
        ("場景赛・デックスハンド", None),
    ]
    for heading, subcategories in categories:
        selected = [item for item in data["competitions"] if (item["Category"] == "场景赛" if subcategories is None else item["Category"] == "竞技赛" and item["Subcategory"] in subcategories)]
        lines.extend([
            f"## {heading}",
            "",
            "| 競技 | 何をするか | 自律・遠隔条件 | 採点 | 優勝Team | 優勝記録・得点 | 出典 |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ])
        for item in selected:
            condition = condition_ja(item)
            winner = item.get("Winner (Gold)") or "未確認"
            result = item.get("Winning result / score") or "未確認"
            result = str(result).replace("（人类世界纪录9.58）", "")
            lines.append(
                f'| {item["Competition ID"]} {item["中文赛项名"]} / {item["日本語説明"]} | '
                f'{TASK_JA[item["Competition ID"]]} | {condition} | {score_ja(item)} | '
                f'{winner} | {result} | {cite(item["Competition ID"])} |'
            )
        lines.append("")
    lines.extend(["## 参考文献", ""])
    for url, (number, title) in refs.items():
        lines.extend([f'<a id="ref-{number}"></a>{number}. [{title}]({url})。', ""])
    return "\n".join(lines)


def scenario_page(data: dict) -> str:
    items = [item for item in data["competitions"] if item["Category"] == "场景赛"]
    lines = [
        "# 場景赛でロボットは何をしたか",
        "",
        "21の场景赛は、単発のデモではなく、複数の物体・道具・指示を含む作業を採点する競技だった。家庭では洗濯や衣類、商超では注文と棚、産業では梱包・組立、デックスハンドでは粉末や豆粒まで扱った。全自律は係数1.0、遠隔操作は0.5で、遠隔操作を禁止した競技と、許可しつつ減点する競技を区別して読む必要がある。[[1]](#ref-1)",
        "",
        "ここでいう21の実環境タスク種目は競技プログラムの数である。閉幕時に発表されたデータセットの『12の応用場面』はデータ分類の数であり、同じ分母ではない。[[2]](#ref-2)",
        "",
        "| 競技・場面 | 実際の作業 | 自律・遠隔 | 採点 | 優勝Team |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f'| {item["Competition ID"]} {item["日本語説明"]} | {TASK_JA[item["Competition ID"]]} | '
            f'{condition_ja(item)} | {score_ja(item)} | {item.get("Winner (Gold)") or "未確認"} |'
        )
    lines.extend([
        "",
        "## 更正を反映した三つの結果",
        "",
        "家庭家政は北京银河星数（305.000点、26分12秒、全自律）、ホテルは优理奇黑豹队（145.000点）、消防救援は上海智元队（150.000点、8分57秒）を最終結果として採用した。いずれも2026年8月23日の公式更正通知を優先し、置き換えられた結果を重複計上していない。[[3]](#ref-3)[[4]](#ref-4)[[5]](#ref-5)",
        "",
        "## 具体例から見える難しさ",
        "",
        "家庭家政は片付けから洗濯・衣類操作までを30分で連結し、途中に宅配受取の指示が入る。商超では反射する袋物を含む商品の把持に加え、誤配置を見つけて戻す判断が必要だった。餐飲では食品を壊さずにつかみ、電子レンジのつまみを操作し、飲料とともに届ける。これらは単一動作の成功率だけでなく、認識、把持、移動、指示追従を長い系列でつなぐ課題だった。[[6]](#ref-6)",
        "",
        "産業の梱包入庫と装配上料では、搬送、識別・仕分け、ラベル、精密挿入を組み合わせた。灵巧手专项赛8競技は、電動工具、粉末、積み木、釘、瓶、箱、ピンセット、ケーブルという異なる接触条件を切り分けて評価した。優勝Teamは智元系が7競技、灵心巧手が1競技だったが、これはTeam名単位の結果であり、全機体の一般性能を示すものではない。[[7]](#ref-7)",
        "",
        "## 参考文献",
        "",
        '<a id="ref-1"></a>1. [世界人形机器人运动会组委会「第二届世界人形机器人运动会竞赛规程总则」](https://www.whrgoc.com/documents/2072500150398033920)（2026年7月2日）。',
        "",
        '<a id="ref-2"></a>2. [中国新闻网「第二届世界人形机器人运动会落幕」](http://www.bj.chinanews.com.cn/news/2026/0827/103275.html)（2026年8月27日）。',
        "",
        '<a id="ref-3"></a>3. [公式「家庭场景-家政服务岗-决赛成绩更正」](https://www.whrgoc.com/resources//uploads/20260823/1787451965643042823.pdf)（2026年8月23日）。',
        "",
        '<a id="ref-4"></a>4. [公式「酒店场景-宾客服务岗-决赛成绩更正」](https://www.whrgoc.com/resources//uploads/20260823/1787451825009048982.pdf)（2026年8月23日）。',
        "",
        '<a id="ref-5"></a>5. [公式「应急场景-消防救援岗-决赛成绩更正」](https://www.whrgoc.com/resources//uploads/20260823/1787451745642097497.pdf)（2026年8月23日）。',
        "",
        '<a id="ref-6"></a>6. [雷峰网「银河通用无遥操完成家庭、餐饮、商超任务」](https://www.leiphone.com/category/ai/U0SX0yIhfMcEsYKm.html)（2026年8月31日）。',
        "",
        '<a id="ref-7"></a>7. [界面新闻「智元机器人赛况与OmniHand专项结果」](https://m.jiemian.com/article/14999667.html)（2026年8月26日）。',
        "",
    ])
    return "\n".join(lines)


def medal_page(data: dict) -> str:
    teams = [item for item in data["team_medals"] if item.get("Rank") is not None]
    lines = [
        "# メダルと主要Team",
        "",
        "組織委員会が一つの再現可能なOrganization別総合メダル表を公表した事実は確認できない。本報告は53の競技・サブ競技単位にある159枠を公式成績公告から再構成し、そのうち136枠を公式Team名へ割り当てた。内訳は金47、銀44、銅45で、23枠（金6、銀9、銅8）は未解決のまま残す。[[1]](#ref-1)",
        "",
        "Team、Organization、Robot manufacturer/platformは同じ単位ではない。したがって主表は、結果公告に直接記載された公式Team名で集計する。企業グループや機体系列への合算は別の分析であり、公式総合表とは呼ばない。",
        "",
        "| 順位 | 公式Team名 | 金 | 銀 | 銅 | 計 |",
        "| ---: | --- | ---: | ---: | ---: | ---: |",
    ]
    for item in teams:
        lines.append(f'| {item["Rank"]} | {item["Official Team Name"]} | {item["Gold"]} | {item["Silver"]} | {item["Bronze"]} | {item["Total"]} |')
    lines.extend([
        "| — | **解決済み合計** | **47** | **44** | **45** | **136** |",
        "| — | **未解決枠** | **6** | **9** | **8** | **23** |",
        "",
        "## メディアの企業集計との違い",
        "",
        "| 報道上の集計 | 公式Team名からの再構成 | 判定 |",
        "| --- | --- | --- |",
        "| 智元 18金・16銀・12銅 | 厳格なTeam名集計は15金・15銀・12銅。拡張規則でも完全一致しない | Partial |",
        "| 北京人形／天工 15金・12銀・18銅 | 金15は逐枠再現。銀10、銅15（拡張規則で銀11、銅16） | Gold reproduced; silver/bronze partial |",
        "| 宇树 10枚 | 宇树科技队は銀2。第三者の宇树プラットフォーム利用Teamを含めても7枚まで | Partial |",
        "",
        "智元の報道値は機体・企業系列、天工は共同研究Teamを含むプラットフォーム系列、宇树は第三者Teamの機体利用まで含む。集計ルールが異なるため、三社の数字を同じOrganization別公式表として比較できない。银河通用については、北京银河星数・宁波具泛智能を関係Teamとみなす明示的規則を置くと3金・1銀・1銅を再現できるが、両Teamとの関係自体に未確認部分が残る。[[2]](#ref-2)[[3]](#ref-3)",
        "",
        "家庭、ホテル、消防は更正後の結果のみを台帳に採用した。更正前の失効結果は二重計上していない。[[4]](#ref-4)",
        "",
        "## 参考文献",
        "",
        '<a id="ref-1"></a>1. [世界人形机器人运动会組織委員会：公式成績公告一覧](https://www.whrgoc.com/announcements)（本調査は個別公告と添付PDFから逐枠再構成）。',
        "",
        '<a id="ref-2"></a>2. [界面新闻「智元18金16銀12銅」](https://m.jiemian.com/article/14999667.html)（2026年8月26日、企業・機体系列の報道集計）。',
        "",
        '<a id="ref-3"></a>3. [钛媒体「智元、天工、银河通用等のメダル集計」](https://www.tmtpost.com/8119366.html)（2026年8月28日、企業合算の説明を含む）。',
        "",
        '<a id="ref-4"></a>4. [公式「8月23日の三つの成績更正」](https://www.whrgoc.com/announcements/2091584626050957312?cid=4ol61bbh)（家庭・ホテル・消防の更正PDFを含む）。',
        "",
    ])
    return "\n".join(lines)


def outputs(data: dict) -> dict[Path, str]:
    return {
        DATA_OUTPUT: json.dumps(data, ensure_ascii=False, indent=2) + "\n",
    }


def main() -> None:
    data = reviewed_data()
    generated = outputs(data)
    if "--check" in sys.argv[1:]:
        stale = [str(path.relative_to(ROOT)) for path, content in generated.items() if not path.exists() or path.read_text(encoding="utf-8") != content]
        if stale:
            print("FAIL: stale generated event report files: " + ", ".join(stale))
            raise SystemExit(1)
        print("OK: generated event evidence is current (51 competitions, 159 medal slots).")
        return
    for path, content in generated.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
