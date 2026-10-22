from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from check_japanese_text import find_issues as find_internal_english
from validate_chinese_chars import find_issues as find_simplified
from validate_terminology import find_issues as find_terminology


class LanguageValidatorTests(unittest.TestCase):
    def sample(self, text: str):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        path = Path(temporary.name) / "sample.md"
        path.write_text(text, encoding="utf-8")
        return path

    def test_forbidden_terminology_negative_control(self):
        path = self.sample("# Test\n\n场景赛 and Team are public prose.\n")
        self.assertTrue(find_terminology([path]))
        self.assertTrue(find_internal_english([path]))
        self.assertTrue(find_simplified([path]))

    def test_marked_names_and_references_are_allowed(self):
        path = self.sample(
            "# 日本語\n\n競技部門と実環境タスク部門を説明する。"
            '<span lang="zh">清华火神队</span>は公式チーム名である。\n\n'
            "## 参考文献\n\n"
            "1. [世界人形机器人运动会](https://example.test)\n"
        )
        self.assertFalse(find_terminology([path]))
        self.assertFalse(find_internal_english([path]))
        self.assertFalse(find_simplified([path]))


if __name__ == "__main__":
    unittest.main()
