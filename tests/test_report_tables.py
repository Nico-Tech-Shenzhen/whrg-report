import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ReportTableTests(unittest.TestCase):
    def test_generated_tables_are_current(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "generate_report_tables.py"), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_public_summary_matches_canonical_entity_counts(self):
        records = json.loads((ROOT / "research" / "evidence" / "records.json").read_text(encoding="utf-8"))
        page = (ROOT / "docs" / "data-tables.md").read_text(encoding="utf-8")
        for entity_type in ("Competition", "Competition Entry", "Team", "Organization", "Robot Platform", "Evidence", "Rule Version"):
            count = sum(record["entity_type"] == entity_type for record in records)
            self.assertIn(f"| {entity_type} | {count} |", page)

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
        known = [item for item in data["medal_ledger"] if item.get("Official Team Name") not in {None, "", "[Unknown]"}]
        self.assertEqual(len(known), 136)
        public = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "docs").glob("*.md"))
        self.assertNotIn("research/staging", public)
        self.assertNotIn("research/imported/kimi", public)
        self.assertNotIn("kimi-event-results-dataset-import", public)


if __name__ == "__main__":
    unittest.main()
