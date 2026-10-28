import json
from pathlib import Path
import re
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ReportTableTests(unittest.TestCase):
    def test_event_report_generation_is_current(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "generate_event_report.py"), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_event_report_counts_and_public_boundaries(self):
        data = json.loads((ROOT / "research" / "evidence" / "event-report-2026.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data["competitions"]), 51)
        self.assertEqual(sum(item["Category"] == "场景赛" for item in data["competitions"]), 21)
        self.assertEqual(len(data["medal_ledger"]), 159)
        known = [item for item in data["medal_ledger"]
                 if item.get("Official Team Name") not in {None, "", "[Unknown]"}]
        self.assertEqual(len(known), 136)
        pages = [ROOT / "docs" / "index.md"]
        pages.extend(ROOT / "docs" / f"ch{number:02d}.md" for number in range(1, 9))
        pages.append(ROOT / "docs" / "appendix.md")
        public = "\n".join(path.read_text(encoding="utf-8") for path in pages)
        self.assertNotIn("research/staging", public)
        self.assertNotIn("research/imported/kimi", public)
        self.assertNotIn("kimi-reader-dataset-terminology-import", public)

    def test_first_time_reader_orientation_and_denominators(self):
        introduction = (ROOT / "docs" / "index.md").read_text(encoding="utf-8")
        chapter_1 = (ROOT / "docs" / "ch01.md").read_text(encoding="utf-8")
        chapter_2 = (ROOT / "docs" / "ch02.md").read_text(encoding="utf-8")
        chapter_3 = (ROOT / "docs" / "ch03.md").read_text(encoding="utf-8")
        chapter_5 = (ROOT / "docs" / "ch05.md").read_text(encoding="utf-8")
        chapter_6 = (ROOT / "docs" / "ch06.md").read_text(encoding="utf-8")

        for token in ("第2回", "北京市人民政府", "有料", "51種目", "1,301"):
            self.assertIn(token, introduction)
        self.assertNotIn("12の応用場面", introduction)
        self.assertIn("競技部門30種目", chapter_1)
        self.assertIn("実環境タスク部門21種目", chapter_1)
        self.assertIn("完全自律", chapter_1)
        self.assertNotIn("五洲大酒店", chapter_1)
        self.assertIn("ロボットの家", chapter_5)
        self.assertIn("五洲大酒店", chapter_5)

        rows = [int(match.group(1)) for match in re.finditer(r"^\| (\d+) \|", chapter_2, re.MULTILINE)]
        self.assertEqual(rows, list(range(1, 52)))
        self.assertIn("自律1.0／遠隔0.5", chapter_2)
        self.assertIn("12の応用場面", chapter_3)
        self.assertIn("21種目", chapter_3)

        canonical_dataset = "12の応用場面、44種類の作業、100種類超の技能、1万件超の詳細タスク"
        self.assertIn(canonical_dataset, chapter_6)
        self.assertNotIn("12種類のモダリティ", chapter_6)
        self.assertNotIn("44行動", chapter_6)

    def test_final_public_structure_has_eight_chapters(self):
        self.assertFalse((ROOT / "docs" / "ch09.md").exists())
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        self.assertNotIn("ch09.md", config)


if __name__ == "__main__":
    unittest.main()
