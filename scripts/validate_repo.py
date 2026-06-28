#!/usr/bin/env python3
from __future__ import annotations

import sys
import re
from pathlib import Path


REQUIRED_TEMPLATE_HEADINGS = [
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

REQUIRED_SKILL_PHRASES = [
    "pasted-text",
    "出海",
    "自媒体运营",
    "--owner-ids me",
    "--page-size 30",
]

REQUIRED_WORKFLOW_PHRASES = [
    "--owner-ids me",
    "--page-size 30",
    "pasted text",
    "failures.jsonl",
    "no Base/Doc/GitHub push",
    "AI硬件/知识/人情世故/大佬分享/饭局闲聊/出海/自媒体运营",
]

REQUIRED_TEMPLATE_PHRASES = [
    "source_mode: feishu-minutes | pasted-text",
    "minute_token: <token | none>",
    "minute_url: <url | none>",
    "基于用户提供的粘贴文本/本地附件",
    "不要把 pasted-text 写成 Feishu 原始妙记",
]

FIRST_CLASS_SCENES = ["出海", "自媒体运营"]
PRIVATE_EXAMPLE_WARNING = "真实复盘仅存于私有 Obsidian 库"
ROBOTS_META = "noindex, nofollow, noarchive, nosnippet"

FORBIDDEN_PUBLIC_EXAMPLE_SUBSTRINGS = [
    ("真实复盘内容", "real meeting deconstruction content"),
]

FORBIDDEN_PUBLIC_EXAMPLE_PATTERNS = [
    (
        re.compile(r"https?://[^\s\])>]+(?:feishu|larksuite)\.cn[^\s\])>]*", re.IGNORECASE),
        "private Feishu/Lark URL",
    ),
    (
        re.compile(r"https?://[^\s\])>]+/(?:minutes|docs|base|wiki|drive)/[^\s\])>]*", re.IGNORECASE),
        "private-looking workspace URL",
    ),
    (
        re.compile(r"\b(?:obcn|omcn|docxcn|bascn)[A-Za-z0-9_-]{8,}\b"),
        "private Feishu token",
    ),
    (
        re.compile(r"(?im)^\s*(?:#{1,6}\s*)?(?:逐字稿|原始逐字稿|Transcript)\s*[:：]?\s*$"),
        "transcript section",
    ),
    (
        re.compile(r"(?im)^\s*(?:发言人|Speaker)\s*[\w一-龥-]*\s*[:：]"),
        "transcript speaker turns",
    ),
    (
        re.compile(r"(?im)^\s*(?:#{1,6}\s*)?(?:人物关系图|人脉关系图|Person map|Relation map)\s*[:：]?\s*$"),
        "person relation map",
    ),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require_file(root: Path, relative: str, errors: list[str]) -> Path:
    path = root / relative
    if not path.exists():
        errors.append(f"missing required file: {relative}")
    return path


def require_phrases(text: str, phrases: list[str], label: str, errors: list[str]) -> None:
    for phrase in phrases:
        if phrase not in text:
            errors.append(f"{label} missing required phrase: {phrase}")


def validate_public_examples(root: Path, errors: list[str]) -> None:
    examples_dir = root / "skills/miaoji-decon/examples"
    if not examples_dir.exists():
        errors.append("missing required directory: skills/miaoji-decon/examples")
        return

    example_files = sorted(path for path in examples_dir.rglob("*") if path.is_file())
    if not example_files:
        errors.append("public examples directory must contain a README policy")
        return

    for path in example_files:
        relative = path.relative_to(root).as_posix()
        text = read_text(path)
        for needle, label in FORBIDDEN_PUBLIC_EXAMPLE_SUBSTRINGS:
            if needle in text:
                errors.append(f"public examples must not contain {label}: {relative}")
        for pattern, label in FORBIDDEN_PUBLIC_EXAMPLE_PATTERNS:
            if pattern.search(text):
                errors.append(f"public examples must not contain {label}: {relative}")


def validate_repo(root: Path) -> list[str]:
    errors: list[str] = []

    skill_path = require_file(root, "skills/miaoji-decon/SKILL.md", errors)
    workflow_path = require_file(root, "skills/miaoji-decon/references/workflow.md", errors)
    template_path = require_file(root, "skills/miaoji-decon/references/template.md", errors)
    examples_path = require_file(root, "skills/miaoji-decon/examples/README.md", errors)
    readme_path = require_file(root, "README.md", errors)
    index_path = require_file(root, "docs/index.html", errors)
    enc_path = require_file(root, "docs/enc.json", errors)

    if errors:
        return errors

    skill_text = read_text(skill_path)
    workflow_text = read_text(workflow_path)
    readme_text = read_text(readme_path)

    require_phrases(skill_text, REQUIRED_SKILL_PHRASES, "SKILL.md", errors)
    require_phrases(workflow_text, REQUIRED_WORKFLOW_PHRASES, "workflow.md", errors)
    template_text = read_text(template_path)
    require_phrases(template_text, REQUIRED_TEMPLATE_HEADINGS, "template.md", errors)
    require_phrases(template_text, REQUIRED_TEMPLATE_PHRASES, "template.md", errors)
    for label, text in [
        ("SKILL.md", skill_text),
        ("workflow.md", workflow_text),
        ("template.md", template_text),
        ("README.md", readme_text),
    ]:
        require_phrases(text, FIRST_CLASS_SCENES, label, errors)

    examples_text = read_text(examples_path)
    if PRIVATE_EXAMPLE_WARNING not in examples_text:
        errors.append("public examples must warn that real deconstructions stay private")
    validate_public_examples(root, errors)

    if ROBOTS_META not in read_text(index_path):
        errors.append("docs/index.html must keep noindex/noarchive robots meta")
    if enc_path.stat().st_size == 0:
        errors.append("docs/enc.json must not be empty")

    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate_repo(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("miaoji-decon repository validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
