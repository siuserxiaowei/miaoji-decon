import importlib.util
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
    "display_name": "siuser小伟",
    "x_url": "https://x.com/_HIT_SZ_",
    "wechat_id": "siuserxiaowei",
}


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
                "X / Twitter：https://x.com/_HIT_SZ_",
                "微信号：siuserxiaowei",
            ]
        )
        self.assertEqual(validate_deconstruction(text, "deep", PROFILE), [])

    def test_missing_wechat_fails(self):
        text = "## 先说结论\n## 来源边界\nX / Twitter：https://x.com/_HIT_SZ_\n"
        errors = validate_deconstruction(text, "quick", PROFILE)
        self.assertTrue(any("WeChat" in error for error in errors))

    def test_quick_does_not_require_deep_sections(self):
        text = (
            "## 先说结论\n## 来源边界\n"
            "X / Twitter：https://x.com/_HIT_SZ_\n微信号：siuserxiaowei\n"
        )
        self.assertEqual(validate_deconstruction(text, "quick", PROFILE), [])

    def test_contact_values_without_labels_fail(self):
        text = (
            "## 先说结论\n## 来源边界\n"
            "https://x.com/_HIT_SZ_\nsiuserxiaowei\n"
        )
        errors = validate_deconstruction(text, "quick", PROFILE)
        self.assertTrue(any("label" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
