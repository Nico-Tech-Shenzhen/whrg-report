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


if __name__ == "__main__":
    unittest.main()
