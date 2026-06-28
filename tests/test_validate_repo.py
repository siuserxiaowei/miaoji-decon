import tempfile
import unittest
from pathlib import Path

from scripts.validate_repo import validate_repo


class ValidateRepoTests(unittest.TestCase):
    def make_repo(self, missing_template_heading=False, public_real_example=False):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        (root / "skills/miaoji-decon/references").mkdir(parents=True)
        (root / "skills/miaoji-decon/examples").mkdir(parents=True)
        (root / "docs").mkdir()

        skill = root / "skills/miaoji-decon/SKILL.md"
        skill.write_text("pasted-text\n出海\n自媒体运营\n--owner-ids me\n--page-size 30\n", encoding="utf-8")

        headings = [
            "## ⏱ 如果只读 10 分钟",
            "## 🎯 这篇真正能学什么",
            "## 🧭 道法术器势（→ 你可以怎么用）",
            "## 📚 深挖：N 个值得单独学的知识点",
            "## 🛠 可直接复用的方法（含\"不要误读成\"）",
            "## 📅 7 天作业",
            "## 🤔 回到自己业务的追问",
            "## 👥 关键人物与资源（这桌人能给你什么）",
            "## 💬 金句",
            "## ⚠️ 来源边界",
        ]
        if missing_template_heading:
            headings.pop()
        (root / "skills/miaoji-decon/references/template.md").write_text("\n".join(headings), encoding="utf-8")

        (root / "skills/miaoji-decon/references/workflow.md").write_text(
            "--owner-ids me\n--page-size 30\npasted text\nfailures.jsonl\n",
            encoding="utf-8",
        )
        example_text = "真实复盘内容" if public_real_example else "真实复盘仅存于私有 Obsidian 库"
        (root / "skills/miaoji-decon/examples/README.md").write_text(example_text, encoding="utf-8")
        (root / "docs/index.html").write_text("noindex, nofollow, noarchive, nosnippet", encoding="utf-8")
        (root / "docs/enc.json").write_text("{}", encoding="utf-8")
        return tmp, root

    def test_valid_repo_has_no_errors(self):
        tmp, root = self.make_repo()
        self.addCleanup(tmp.cleanup)
        self.assertEqual(validate_repo(root), [])

    def test_missing_template_heading_is_error(self):
        tmp, root = self.make_repo(missing_template_heading=True)
        self.addCleanup(tmp.cleanup)
        errors = validate_repo(root)
        self.assertTrue(any("来源边界" in error for error in errors))

    def test_public_real_example_is_error(self):
        tmp, root = self.make_repo(public_real_example=True)
        self.addCleanup(tmp.cleanup)
        errors = validate_repo(root)
        self.assertTrue(any("public examples" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
