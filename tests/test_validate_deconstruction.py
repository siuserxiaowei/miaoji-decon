import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills/miaoji-decon/scripts/validate_deconstruction.py"
)
SPEC = importlib.util.spec_from_file_location("miaoji_validate_deconstruction", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)
validate_deconstruction = MODULE.validate_deconstruction


PROFILE = {
    "display_name": "示例作者",
    "x_url": "https://x.com/example_user",
    "wechat_id": "example_wechat",
}

EMPTY_PROFILE = {"display_name": "", "x_url": "", "wechat_id": ""}


class ValidateDeconstructionTests(unittest.TestCase):
    def test_deep_output_with_signature_passes(self):
        text = "\n".join(
            [
                "## 先说结论",
                "## 来源边界",
                "## 可信度总览",
                "## 道法术器势",
                "## 7 天实践",
                "## 材料与证据口径",
                "## 共识与分歧",
                "## 反方审计",
                "## 来源与时间码索引",
                "X / Twitter：https://x.com/example_user",
                "微信号：example_wechat",
            ]
        )
        self.assertEqual(validate_deconstruction(text, "deep", PROFILE), [])

    def test_missing_wechat_fails(self):
        text = "## 先说结论\n## 来源边界\nX / Twitter：https://x.com/example_user\n"
        errors = validate_deconstruction(text, "quick", PROFILE)
        self.assertTrue(any("WeChat" in error for error in errors))

    def test_quick_does_not_require_deep_sections(self):
        text = (
            "## 先说结论\n## 来源边界\n"
            "X / Twitter：https://x.com/example_user\n微信号：example_wechat\n"
        )
        self.assertEqual(validate_deconstruction(text, "quick", PROFILE), [])

    def test_contact_values_without_labels_fail(self):
        text = (
            "## 先说结论\n## 来源边界\n"
            "https://x.com/example_user\nexample_wechat\n"
        )
        errors = validate_deconstruction(text, "quick", PROFILE)
        self.assertTrue(any("label" in error for error in errors))

    def test_section_name_in_body_without_heading_fails(self):
        # 章节名只出现在正文引用中（非 Markdown 标题）时不得误判为已有该章节
        text = (
            "本文会在后面讨论先说结论与来源边界。\n"
            "X / Twitter：https://x.com/example_user\n微信号：example_wechat\n"
        )
        errors = validate_deconstruction(text, "quick", PROFILE)
        self.assertTrue(any("先说结论" in error for error in errors))
        self.assertTrue(any("来源边界" in error for error in errors))

    def test_placeholder_tokens_fail(self):
        for placeholder in ["TODO", "TBD", "XXX", "{标题}", "｛标题｝"]:
            text = (
                f"## 先说结论\n{placeholder}\n## 来源边界\n"
                "X / Twitter：https://x.com/example_user\n微信号：example_wechat\n"
            )
            errors = validate_deconstruction(text, "quick", PROFILE)
            self.assertTrue(
                any("placeholder" in error for error in errors),
                f"placeholder not detected: {placeholder}",
            )

    def test_banned_terms_fail(self):
        text = (
            "## 先说结论\n星辰科技的做法值得学习。\n## 来源边界\n"
            "X / Twitter：https://x.com/example_user\n微信号：example_wechat\n"
        )
        errors = validate_deconstruction(
            text, "quick", PROFILE, banned_terms=["星辰科技"]
        )
        self.assertTrue(any("banned term" in error for error in errors))

    def test_banned_terms_mapping_keys_fail(self):
        # redactions.json 风格的映射对象取其键作为敏感词表
        mapping = {"星辰科技": "某硬件公司", "某集团客户实名": "某集团客户"}
        with tempfile.NamedTemporaryFile(
            "w", suffix=".json", delete=False, encoding="utf-8"
        ) as fh:
            json.dump(mapping, fh, ensure_ascii=False)
            temp_path = Path(fh.name)
        try:
            terms = MODULE.load_banned_terms(temp_path)
        finally:
            temp_path.unlink()
        self.assertEqual(terms, ["星辰科技", "某集团客户实名"])

        text = (
            "## 先说结论\n某集团客户实名已确认合作。\n## 来源边界\n"
            "X / Twitter：https://x.com/example_user\n微信号：example_wechat\n"
        )
        errors = validate_deconstruction(text, "quick", PROFILE, banned_terms=terms)
        self.assertTrue(any("banned term" in error for error in errors))

    def test_redacted_output_with_banned_terms_passes(self):
        text = (
            "## 先说结论\n某硬件公司的做法值得学习。\n## 来源边界\n"
            "X / Twitter：https://x.com/example_user\n微信号：example_wechat\n"
        )
        self.assertEqual(
            validate_deconstruction(
                text, "quick", PROFILE, banned_terms=["星辰科技"]
            ),
            [],
        )

    def test_unconfigured_profile_skips_signature_checks(self):
        # 默认空模板（使用者未配置自己的联系方式）时，无署名也应通过
        text = "## 先说结论\n## 来源边界\n"
        self.assertEqual(validate_deconstruction(text, "quick", EMPTY_PROFILE), [])

    def test_configured_profile_still_enforces_signature(self):
        text = "## 先说结论\n## 来源边界\n"
        errors = validate_deconstruction(text, "quick", PROFILE)
        self.assertTrue(any("X / Twitter" in error for error in errors))
        self.assertTrue(any("WeChat" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
