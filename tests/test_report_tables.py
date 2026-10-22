import json
from pathlib import Path
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
        pages.extend(ROOT / "docs" / f"ch{number:02d}.md" for number in range(1, 10))
        pages.append(ROOT / "docs" / "appendix.md")
        public = "\n".join(path.read_text(encoding="utf-8") for path in pages)
        self.assertNotIn("research/staging", public)
        self.assertNotIn("research/imported/kimi", public)
        self.assertNotIn("kimi-reader-dataset-terminology-import", public)


if __name__ == "__main__":
    unittest.main()
