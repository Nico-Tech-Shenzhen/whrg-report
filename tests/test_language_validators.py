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

    def test_noncanonical_company_alias_is_rejected(self):
        path = self.sample("# 日本語\n\n加速進化は機体を提供した。\n")
        issues = find_terminology([path])
        self.assertTrue(issues)
        self.assertEqual(issues[0][2], "加速進化")
        self.assertEqual(issues[0][3], "Booster Robotics")

    def test_official_team_product_and_dataset_names_are_allowed(self):
        path = self.sample(
            "# 日本語\n\n"
            '<span lang="zh">北京智元赛队</span>は公式チーム名である。'
            "Booster T2、Unitree G1、Linker Handを機体・製品名として使う。"
            "AgiBot World 2026はデータセット名である。\n"
        )
        self.assertFalse(find_terminology([path]))

    def test_source_title_and_legal_annotation_are_allowed(self):
        path = self.sample(
            "# 日本語\n\n"
            'Spirit AI（法的主体：<span lang="zh">万境千寻（北京）科技有限公司</span>）を確認した。\n\n'
            "## 参考文献\n\n"
            "1. [智元机器人发布消息](https://example.test)\n"
        )
        self.assertFalse(find_terminology([path]))


if __name__ == "__main__":
    unittest.main()
