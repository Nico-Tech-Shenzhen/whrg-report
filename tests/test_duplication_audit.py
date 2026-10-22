import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DuplicationAuditTests(unittest.TestCase):
    def test_audit_runs_and_finds_no_exact_cross_page_paragraphs(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "audit_public_duplication.py"), "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["files"], 10)
        self.assertEqual(payload["exact"], [])


if __name__ == "__main__":
    unittest.main()
