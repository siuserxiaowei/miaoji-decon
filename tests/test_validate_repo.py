import json
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
        (root / "skills/miaoji-decon/assets").mkdir(parents=True)
        (root / "skills/miaoji-decon/agents").mkdir(parents=True)
        (root / "skills/miaoji-decon/scripts").mkdir(parents=True)
        (root / "docs").mkdir()

        skill = root / "skills/miaoji-decon/SKILL.md"
        skill.write_text(
            "pasted-text\nsource-pack\n出海\n自媒体运营\n--owner-ids me\n--page-size 30\n"
            "assets/author-profile.json\nscripts/validate_deconstruction.py\n",
            encoding="utf-8",
        )
        (root / "README.md").write_text("出海\n自媒体运营\n", encoding="utf-8")

        headings = [
            "## 先说结论",
            "## 🧾 材料与证据口径",
            "## 🚦 可信度总览",
            "## ⏱ 如果只读 10 分钟",
            "## 🎯 这篇真正能学什么",
            "## 🧭 道法术器势（→ 你可以怎么用）",
            "## 📚 深挖：N 个值得单独学的知识点",
            "## 🛠 可直接复用的方法",
            "## 📅 给没参加 / 没看过的人的 7 天实践",
            "## 🤔 回到自己业务的追问",
            "## 👥 关键人物与资源",
            "## 💬 金句",
            "## 🔎 来源与时间码索引",
            "## ⚠️ 来源边界",
        ]
        if missing_template_heading:
            headings.pop()
        template_phrases = [
            "出海",
            "自媒体运营",
            "source_mode: feishu-minutes | pasted-text | source-pack",
            "minute_token: <token | none>",
            "minute_url: <url | none>",
            "不要把 pasted-text 写成 Feishu 原始妙记",
            "基于用户提供的粘贴文本/本地附件",
            "https://x.com/_HIT_SZ_",
            "siuserxiaowei",
        ]
        (root / "skills/miaoji-decon/references/template.md").write_text(
            "\n".join(headings + template_phrases),
            encoding="utf-8",
        )

        (root / "skills/miaoji-decon/references/workflow.md").write_text(
            "--owner-ids me\n--page-size 30\npasted text\nfailures.jsonl\n"
            "no Base/Doc/GitHub push\n"
            "AI硬件/知识/人情世故/大佬分享/饭局闲聊/出海/自媒体运营\n"
            "source pack\nvalidate_deconstruction.py\n",
            encoding="utf-8",
        )
        (root / "skills/miaoji-decon/references/evidence-protocol.md").write_text(
            "来源家族\n主张台账\n高可信\n中可信\n低可信\n启动不等于完成\n",
            encoding="utf-8",
        )
        (root / "skills/miaoji-decon/assets/author-profile.json").write_text(
            json.dumps(
                {
                    "display_name": "siuser小伟",
                    "x_url": "https://x.com/_HIT_SZ_",
                    "wechat_id": "siuserxiaowei",
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        (root / "skills/miaoji-decon/agents/openai.yaml").write_text(
            'default_prompt: "Use $miaoji-decon"\nallow_implicit_invocation: true\n',
            encoding="utf-8",
        )
        (root / "skills/miaoji-decon/scripts/validate_deconstruction.py").write_text(
            "x_url\nwechat_id\n",
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

    def test_public_private_looking_extra_example_is_error(self):
        tmp, root = self.make_repo()
        self.addCleanup(tmp.cleanup)
        (root / "skills/miaoji-decon/examples/leaky.md").write_text(
            "# Synthetic leak guard\n"
            "## 逐字稿\n"
            "发言人A：这里是合成占位内容。\n"
            "https://example.invalid/minutes/obcnSYNTHETIC0000\n"
            "## 人物关系图\n"
            "A -> B\n",
            encoding="utf-8",
        )
        errors = validate_repo(root)
        self.assertTrue(any("public examples" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
