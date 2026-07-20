#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


COMMON_SECTIONS = ["先说结论", "来源边界"]
STANDARD_SECTIONS = ["可信度总览", "道法术器势", "7 天"]
DEEP_SECTIONS = ["材料与证据口径", "共识与分歧", "反方审计", "来源与时间码索引"]

# 占位符：TODO / TBD / XXX / 半角与全角花括号占位（如 {标题} / ｛标题｝）
PLACEHOLDER_PATTERNS = [
    re.compile(r"\bTODO\b"),
    re.compile(r"\bTBD\b"),
    re.compile(r"\bXXX\b"),
    re.compile(r"\{[^{}\n]*[一-鿿][^{}\n]*\}"),
    re.compile(r"｛[^｛｝\n]*[一-鿿][^｛｝\n]*｝"),
]


def load_profile(path: Path) -> dict[str, str]:
    return json.loads(path.read_text(encoding="utf-8"))


def profile_configured(profile: dict[str, str]) -> bool:
    """使用者已填写自己的联系方式时才强制署名校验；默认空模板表示未配置。"""
    return bool(profile.get("x_url") and profile.get("wechat_id"))


def load_banned_terms(path: Path) -> list[str]:
    """接受字符串数组 JSON，或 redactions.json 那样的映射对象（取其键）。"""
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        terms = list(data.keys())
    elif isinstance(data, list):
        terms = data
    else:
        raise ValueError("banned-terms JSON must be a string array or a mapping object")
    terms = [term for term in terms if isinstance(term, str) and term]
    if not terms:
        raise ValueError("banned-terms JSON contains no usable string terms")
    return terms


def has_section_heading(text: str, section: str) -> bool:
    """Markdown 标题级匹配（^#{1,6} ... 章节名），避免正文引用造成误判。"""
    pattern = rf"^#{{1,6}}\s*.*{re.escape(section)}"
    return re.search(pattern, text, flags=re.MULTILINE) is not None


def validate_deconstruction(
    text: str,
    mode: str,
    profile: dict[str, str],
    banned_terms: list[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    required = list(COMMON_SECTIONS)
    if mode in {"standard", "deep"}:
        required.extend(STANDARD_SECTIONS)
    if mode == "deep":
        required.extend(DEEP_SECTIONS)

    for section in required:
        if not has_section_heading(text, section):
            errors.append(f"missing required section heading for {mode} mode: {section}")

    for pattern in PLACEHOLDER_PATTERNS:
        match = pattern.search(text)
        if match:
            errors.append(f"unresolved placeholder left in output: {match.group(0)}")

    for term in banned_terms or []:
        if term in text:
            errors.append(f"banned term present in output: {term}")

    if profile_configured(profile):
        if "X / Twitter" not in text:
            errors.append("missing visible X / Twitter label")
        if profile["x_url"] not in text:
            errors.append(f"missing configured X / Twitter URL: {profile['x_url']}")
        if "微信号" not in text:
            errors.append("missing visible WeChat label: 微信号")
        if profile["wechat_id"] not in text:
            errors.append(f"missing configured WeChat ID: {profile['wechat_id']}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a miaoji-decon output before publishing")
    parser.add_argument("file", type=Path)
    parser.add_argument("--mode", choices=["quick", "standard", "deep"], default="standard")
    parser.add_argument(
        "--banned-terms",
        type=Path,
        default=None,
        help="JSON file: string array, or a redactions.json-style mapping object (its keys are used)",
    )
    parser.add_argument(
        "--author-profile",
        type=Path,
        default=None,
        help="author profile JSON; defaults to the skill's assets/author-profile.json",
    )
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    profile_path = args.author_profile or (skill_root / "assets/author-profile.json")
    profile = load_profile(profile_path)
    text = args.file.read_text(encoding="utf-8")
    banned_terms = load_banned_terms(args.banned_terms) if args.banned_terms else None
    errors = validate_deconstruction(text, args.mode, profile, banned_terms=banned_terms)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    if not profile_configured(profile):
        print("author profile not configured, skipping signature checks")
    print(f"deconstruction validation passed ({args.mode})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
