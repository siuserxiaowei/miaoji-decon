#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


COMMON_SECTIONS = ["先说结论", "来源边界"]
STANDARD_SECTIONS = ["可信度总览", "道法术器势", "7 天"]
DEEP_SECTIONS = ["材料与证据口径", "共识与分歧", "反方审计", "来源与时间码索引"]


def load_profile(skill_root: Path) -> dict[str, str]:
    path = skill_root / "assets/author-profile.json"
    return json.loads(path.read_text(encoding="utf-8"))


def validate_deconstruction(text: str, mode: str, profile: dict[str, str]) -> list[str]:
    errors: list[str] = []
    required = list(COMMON_SECTIONS)
    if mode in {"standard", "deep"}:
        required.extend(STANDARD_SECTIONS)
    if mode == "deep":
        required.extend(DEEP_SECTIONS)

    for section in required:
        if section not in text:
            errors.append(f"missing required section or marker for {mode} mode: {section}")

    if "X / Twitter" not in text:
        errors.append("missing visible X / Twitter label")
    if profile["x_url"] not in text:
        errors.append(f"missing fixed X / Twitter URL: {profile['x_url']}")
    if "微信号" not in text:
        errors.append("missing visible WeChat label: 微信号")
    if profile["wechat_id"] not in text:
        errors.append(f"missing fixed WeChat ID: {profile['wechat_id']}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a miaoji-decon output before publishing")
    parser.add_argument("file", type=Path)
    parser.add_argument("--mode", choices=["quick", "standard", "deep"], default="standard")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    profile = load_profile(skill_root)
    text = args.file.read_text(encoding="utf-8")
    errors = validate_deconstruction(text, args.mode, profile)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"deconstruction validation passed ({args.mode})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
